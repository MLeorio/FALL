# FALL & PUPA - FastAPI APP

API pour l'application mobile des objets trouv&eacute;s et perdus
```
{"Hi": "Fall&Pupa"}
```

## D&eacute;ploiement sur Cyclic en quelques secondes

[![Deploy to Cyclic](https://deploy.cyclic.app/button.svg)](https://deploy.cyclic.app/)

Definir `server.py` comme point d'entrée de l'application.

## Ex&eacute;cution en locale

Prérequis:
- Environnement virtuel : .env
- python > 3.10.11

Installation :
- crée un environement virtuel : `python3 venv nom_de_environement`
- Installer les dépendances depuis  le fichier requirements.txt : `pip install -r requirements.txt`

Lancement:
- activer l'environnement virtuel : `source nom_de_environnement/script/activate`
- lancer la commande suivante : `uvicorn main:app --reload` ou plus simplement `python server.py`

## Essayer le serveur

Documentation de l'API: [http://localhost:8181](http://localhost:8181)


# Enjoy guys