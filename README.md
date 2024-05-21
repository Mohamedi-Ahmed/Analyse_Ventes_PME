# Analyser les Ventes d’une PME

Ce projet a été réalisé dans le cadre de la préparation à la journée de sélection pour le parcours de formation Data Engineer chez SIMPLON.CO. L'objectif est de créer une architecture permettant l'importation, le stockage et l'analyse des données de ventes d'une PME.

## Objectifs

- Créer et mettre en œuvre une architecture à deux services :
  - Un service pour l’exécution des scripts d'importation de données.
  - Un service pour le stockage des données en base de données SQLite.
- Analyser un jeu de données et en expliquer les caractéristiques.
- Créer une base de données adaptée pour le stockage des données de ventes.
- Réaliser une première analyse des données avec SQL.
- Stocker les résultats des analyses.

## Structure du Projet

### 1. Conception de l’architecture

L'architecture du projet comprend deux services :

- **Service d'exécution des scripts** (`script-runner`)
  - Objectif : Exécuter les scripts pour importer et analyser les données.
- **Service de stockage des données** (`database`)
  - Objectif : Stocker les données dans une base de données SQLite.

Les services communiquent entre eux via des ports exposés et définis dans le fichier `docker-compose.yml`.

### 2. Réalisation de l’architecture

- **Dockerfile pour le service d'exécution des scripts**
  ```dockerfile
  # Utiliser une image de base Python
  FROM python:3.9

  # Définir le répertoire de travail
  WORKDIR /app

  # Copier le script dans le conteneur
  COPY script.py .

  # Installer les dépendances nécessaires
  RUN pip install requests sqlite3

  # Commande pour exécuter le script
  CMD ["python", "script.py"]
