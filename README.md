# Assistant local

Assistant Python : Ollama, recherche web Tavily, lecture et création de fichiers, génération d’images.

## Installation sur Windows

Prérequis : Python 3.11 ou 3.12 et [Ollama](https://ollama.com). Téléchargez le dépôt, puis ouvrez PowerShell dans son dossier.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
ollama pull qwen3:4b
```

Dans `.env`, renseignez votre nouvelle clé après `TAVILY_API_KEY=`. Sans clé, le chat reste disponible mais la recherche web est désactivée. Démarrez Ollama (application ou `ollama serve`), puis :

```powershell
.\.venv\Scripts\python.exe main.py
```

Tapez `quit` pour quitter. Modifiez `OLLAMA_MODEL` dans `.env` pour changer de modèle.

## Utilisation

- « Recherche des informations sur Python et cite tes sources. »
- « Enregistre un texte de bienvenue dans bienvenue.txt. »
- « Résume le fichier notes.txt. »

Placez les fichiers à lire dans `workspace/` (créé au lancement). Les chemins hors de ce dossier sont refusés ; la lecture est limitée à 1 Mo. La création refuse d’écraser un fichier existant. Ces protections ne constituent pas une isolation face aux autres programmes locaux.

## Images 

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-images.txt
```

## Références

- [Ollama : fonctions comme outils](https://ollama.com/blog/functions-as-tools)
- [Diffusers : pipelines](https://huggingface.co/docs/diffusers/main/api/pipelines/overview)
