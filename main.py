from ollama import chat

from tavily import TavilyClient

from pprint import pprint

from datetime import date

import torch

from diffusers import DiffusionPipeline



tavily = TavilyClient(api_key="Votre clé api")



def rechercheweb(question):

    resultat = tavily.search(query=question)

    return resultat



def enregistrefichier(nom_fichier, txt):

    fichier = open(nom_fichier, "w", encoding="utf-8")

    fichier.write(txt)

    fichier.close()

    return "Fichier enregistré :" + nom_fichier



def lire_fichier(nom_fichier):

    fichier=open(nom_fichier,"r",encoding="utf-8")

    texte=fichier.read()

    fichier.close()

    return texte





demande = input("comment je puisse vous aider aujourd'hui ?")

L = []



def memoire(role, contenu):

    L.append({

        "role": role,

        "content": contenu

    })



generateur = DiffusionPipeline.from_pretrained(

    "stable-diffusion-v1-5/stable-diffusion-v1-5",

    dtype=torch.float16,

    use_safetensors=True

)

generateur = generateur.to("cuda")

def genereimage(description):

    image = generateur(prompt=description).images[0]

    image.show()





while demande.lower() != "quit":

    memoire("user", demande)



    try:

        agent = chat(

            model="qwen3:4b",

            messages=L,

            tools=[rechercheweb,enregistrefichier,lire_fichier,genereimage],

        )

    except ConnectionError:

        print("impossible de se connecter à ollama, lancez ollama serve.")

        continue



    reponse = agent.message.content



    if agent.message.tool_calls:

        for i in agent.message.tool_calls:



            if i.function.name == "rechercheweb":

                question = i.function.arguments["question"]

                cherche = rechercheweb(question)



                if cherche["results"]:

                    resultat = (

                        cherche["results"][0]["title"] + "\n"

                        + cherche["results"][0]["content"] + "\n"

                        + cherche["results"][0]["url"]

                    )

                    

                    agent = chat(

                        model="qwen3:4b",

                        messages=L+[

                            {

                                "role": "user",

                                "content": (

                                    "nous somme le "

                                    + str(date.today()) + "\n"

                                    + "réponds à la question à partir des "

                                    + "information web ci-dessous.\n"

                                    + "elles peuvent être plus récentes "

                                    + "que tes connaissances\n"

                                    + "si les informations du web ne sont "

                                    + "pas suffisantes, évite de répondre "

                                    + "au hasard mais plutot précises "

                                    + "qu'il manque des informations "

                                    + "pour répondre\n"

                                    + "Réponds en une ou deux phrases, "

                                    + "sans répétition ni commentaire "

                                    + "sur la date.\n"

                                    + "question :" + demande + "\n"

                                    + "information web :" + resultat

                                )

                            }

                        ],

                    )



                    reponse = agent.message.content



                else:

                    reponse = "Aucun résultat trouvé pour ta demande"





            elif i.function.name == "enregistrefichier":

                nom_fichier = i.function.arguments["nom_fichier"]

                txt = i.function.arguments["txt"]

                reponse = enregistrefichier(nom_fichier, txt)





            elif i.function.name == "lire_fichier":

                a = input("ecris le nom complet du fichier")

                try:

                    texte_lu = lire_fichier(a)

                    agent = chat(

                        model="qwen3:4b",

                        messages=[

                            {

                                "role": "user",

                                "content": (

                                    "tu dois résumer le texte du fichier\n"

                                    + "en gardant les informations nécessaires et importantes\n"

                                    + "le texte du fichier :" + texte_lu

                                )

                            }

                         ]

                    )

                    reponse = agent.message.content

                except FileNotFoundError:

                    reponse = "Ce fichier n'existe pas."



            elif i.function.name=="genereimage": 

                description = i.function.arguments["description"]

                genereimage(description)

                reponse = "L'image a été générée et ouverte."

 





    memoire("assistant", reponse)

    print(reponse)

    demande = input("Une autre question ? (quit pour arrêter) : ")
