# Blockchain Practice

Ce dépôt contient plusieurs exercices réalisés dans le cadre de l'unité Blockchain. Les exercices exploitent l'API Blockstream (Esplora) pour interroger la blockchain Bitcoin et mettre en œuvre diverses fonctionnalités, notamment :

- La récupération et l'analyse des transactions d'un bloc
- L'extraction d'informations (par exemple, l'adresse Bitcoin la plus fréquente sur un intervalle de blocs)
- La vérification de la preuve de Merkle d'une transaction


## Prérequis

- Python 3.7 ou supérieur
- Git
- Connexion Internet (pour interroger l'API Blockstream)

## Installation

1. Clonez ce dépôt :

    ```bash
    git clone https://github.com/tarekatbi/blockchain_practice.git
    cd blockchain_practice
    ```

2. Créez et activez un environnement virtuel :

    ```bash
    python -m venv myenv
    # Sur macOS/Linux :
    source myenv/bin/activate
    # Sur Windows :
    .\myenv\Scripts\activate
    ```

3. Installez les dépendances :

    ```bash
    pip install -r requirements.txt
    ```

## Utilisation

Chaque exercice se trouve dans son propre répertoire. Par exemple :

- **Exercice 1 :** Récupère la transaction avec le plus gros montant échangé dans un bloc.

    ```bash
    python exo1/app.py <block_hash>
    ```

- **Exercice 2 :** Analyse un intervalle de blocs et affiche l'adresse Bitcoin la plus fréquente.

    ```bash
    python exo2/app.py <h1> <h2>
    ```

- **Exercice 3 :** Vérifie la preuve de Merkle pour une transaction donnée dans un bloc.

    ```bash
    python exo3/app.py <block_hash> <txid>
    ```

## Contribution

Les contributions et suggestions d'amélioration sont les bienvenues. N'hésitez pas à ouvrir une issue ou à proposer un pull request.

## Licence

Ce projet est sous licence MIT.
