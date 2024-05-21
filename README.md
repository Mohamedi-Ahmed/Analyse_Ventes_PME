# Projet : Analyser les ventes d’une PME

Ce projet a été réalisé pour préparer la journée de sélection pour le parcours de formation Data Engineer chez Simplon. Il consiste à analyser les ventes d'une PME en mettant en place une architecture en deux services avec Docker et en utilisant SQLite comme base de données.

## Objectifs

- Créer et mettre en œuvre une architecture en deux services : un pour l’exécution des scripts et un autre pour la base de données.
- Analyser un jeu de données et en expliquer ses caractéristiques.
- Créer une base de données adaptée pour le stockage du jeu de données.
- Importer les données.
- Réaliser une première analyse des données avec SQL.
- Stocker les résultats des analyses.

## Architecture

L'architecture du projet comprend deux services principaux :
1. **Service d'exécution des scripts** (`script-runner`): Ce service est responsable de l'exécution des scripts pour importer et analyser les données.
2. **Service de stockage des données** (`database`): Ce service utilise SQLite pour stocker les données importées.

Les services communiquent entre eux via des ports exposés.

## Fichiers du projet

- **Dockerfile** : Fichier pour construire l'image Docker du service d'exécution des scripts.
- **docker-compose.yml** : Fichier Docker Compose pour orchestrer les deux services.
- **script.py** : Script Python pour l'importation et l'analyse des données.
- **schema.sql** : Fichier SQL pour créer les tables de la base de données.

## Installation

1. Clonez ce dépôt :
    ```sh
    git clone https://github.com/votre-utilisateur/analyser-les-ventes-pme.git
    cd analyser-les-ventes-pme
    ```

2. Construisez et démarrez les conteneurs Docker :
    ```sh
    docker-compose up --build
    ```

## Utilisation

1. **Importer les données** :
   - Les données sont importées automatiquement depuis les URLs fournies dans le script `script.py`.

2. **Analyser les données** :
   - Les requêtes SQL pour analyser les ventes sont exécutées via le script Python et les résultats sont stockés dans la base de données SQLite.

## Scripts

- **script.py** :
  - Collecte les fichiers de données à partir des URLs partagées par le client.
  - Crée la base de données et les tables nécessaires.
  - Importe les nouvelles données de vente.
  - Exécute des requêtes SQL pour obtenir le chiffre d'affaires total, les ventes par produit et les ventes par région.

## Exemples de Requêtes SQL

- Chiffre d'affaires total :
  ```sql
  SELECT SUM(total) FROM ventes;
