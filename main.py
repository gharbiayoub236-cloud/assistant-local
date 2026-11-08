from ollama import chat
from tavily import TavilyClient
from datetime import date
import torch
from diffusers import DiffusionPipeline

tavily = TavilyClient(api_key="clé api")

L = []


def rechercheweb(question):
    resultat = tavily.search(query=question)
    return resultat


def enregistrefichier(nom_fichier, txt):
    fichier = open(nom_fichier, "w", encoding="utf-8")
    fichier.write(txt)
    fichier.close()
    return "Fichier enregistré :" + nom_fichier


def lire_fichier(nom_fichier):
    fichier = open(nom_fichier, "r", encoding="utf-8")
    texte = fichier.read()
    fichier.close()
    return texte


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


def repondre_agent(demande):
    memoire("user", demande)

    try:
        agent = chat(
            model="qwen3:4b",
            messages=[
    {
        "role": "system",
        "content": (
            "Tu es Ayoub IA. Réponds naturellement en français "
            "et utilise l'historique de la conversation. "
            "Utilise les outils uniquement quand la demande le nécessite. "
            "Crée un fichier seulement si l'utilisateur le demande explicitement. "
            "Une information personnelle doit simplement être prise "
            "en compte dans la conversation."
             )
            }
            ] + L,
            tools=[
                rechercheweb,
                enregistrefichier,
                lire_fichier,
                genereimage
            ],
        )
    except ConnectionError:
        return "Impossible de se connecter à Ollama. Lance Ollama."

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
                        messages=L + [
                            {
                                "role": "user",
                                "content": (
                                    "Nous sommes le "
                                    + str(date.today()) + "\n"
                                    + "Réponds à la question à partir des "
                                    + "informations web ci-dessous.\n"
                                    + "Elles peuvent être plus récentes "
                                    + "que tes connaissances.\n"
                                    + "Si les informations du web ne sont "
                                    + "pas suffisantes, évite de répondre "
                                    + "au hasard mais précise "
                                    + "qu'il manque des informations "
                                    + "pour répondre.\n"
                                    + "Réponds en une ou deux phrases, "
                                    + "sans répétition ni commentaire "
                                    + "sur la date.\n"
                                    + "Question : " + demande + "\n"
                                    + "Informations web : " + resultat
                                )
                            }
                        ],
                    )

                    reponse = agent.message.content

                else:
                    reponse = "Aucun résultat trouvé pour ta demande."

            elif i.function.name == "enregistrefichier":
                nom_fichier = i.function.arguments["nom_fichier"]
                txt = i.function.arguments["txt"]
                reponse = enregistrefichier(nom_fichier, txt)

            elif i.function.name == "lire_fichier":
                nom_fichier = i.function.arguments["nom_fichier"]

                try:
                    texte_lu = lire_fichier(nom_fichier)

                    agent = chat(
                        model="qwen3:4b",
                        messages=[
                            {
                                "role": "user",
                                "content": (
                                    "Tu dois résumer le texte du fichier\n"
                                    + "en gardant les informations "
                                    + "nécessaires et importantes.\n"
                                    + "Le texte du fichier : " + texte_lu
                                )
                            }
                        ],
                    )

                    reponse = agent.message.content

                except FileNotFoundError:
                    reponse = "Ce fichier n'existe pas."

            elif i.function.name == "genereimage":
                description = i.function.arguments["description"]
                genereimage(description)
                reponse = "L'image a été générée et ouverte."

    memoire("assistant", reponse)
    return reponse
