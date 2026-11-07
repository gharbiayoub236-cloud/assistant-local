# Assistant local

Assistant Python en français : Ollama, recherche web Tavily, lecture et création de fichiers, génération d’images facultative.

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

## Images facultatives

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-images.txt
```

Définissez `ENABLE_IMAGES=true` dans `.env`, puis demandez une image. Stable Diffusion sera téléchargé au premier appel (plusieurs Go). Les images sont enregistrées dans `workspace/images/`. Un GPU NVIDIA compatible CUDA est recommandé ; le CPU fonctionne mais est lent. Installez au besoin la version de [PyTorch adaptée à votre GPU](https://pytorch.org/get-started/locally/).

## Sécurité et confidentialité

Aucune clé API n’est incluse dans ce dépôt. `.env` et `workspace/` sont exclus de Git. Révoquez toute clé déjà partagée, puis utilisez une nouvelle clé uniquement dans votre `.env` local. Ne publiez jamais ce fichier.

Ollama utilise le modèle local téléchargé. Les recherches sont envoyées à Tavily et leurs extraits sont ensuite traités par le modèle local.

## Vérification

```powershell
python -m unittest discover -s tests -v
```

Les tests utilisent des outils simulés, sans clé API ni GPU. Les appels réels à Tavily et la génération d’images nécessitent votre configuration locale.

## Références

- [Ollama : fonctions comme outils](https://ollama.com/blog/functions-as-tools)
- [Diffusers : pipelines](https://huggingface.co/docs/diffusers/main/api/pipelines/overview)
