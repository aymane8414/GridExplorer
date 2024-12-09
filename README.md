# Projet IA

## Description du projet 

Ce projet met en œuvre un algorithme de Q-Learning dans un environnement simulé avec obstacles, visant à optimiser les déplacements d'une voiture à travers une grille en évitant les obstacles, tout en maximisant les récompenses jusqu'à atteindre une case finale. Une courbe d'apprentissage est générée automatiquement pour visualiser l'évolution des performances.

## Commandes pour commencer le projet

Pour commencer avec ce projet, suivez les étapes ci-dessous :


2. Accédez au répertoire du projet :

```sh
cd Q_Learning
```

3. Installez les dépendances :

```sh
pip install -r requirements.txt
```

4. Lancez la simulation :

```sh
python main.py
```
## Structure des fichiers

- **main.py** : Script principal pour lancer la simulation
- **q_learning.py** : Implémentation de l'algorithme Q-Learning
- **car.py** : Modélisation de la voiture et gestion de ses capteurs
- **utils.py** : Fonctions utilitaires (génération de la grille, obstacles, et création de la courbe)
- **requirements.txt** : Liste des dépendances Python nécessaires.

### Paramètres d'apprentissage

- **Alpha** : Taux d'apprentissage, ajuste la rapidité d'adaptation.
- **Gamma** : Facteur d'actualisation, pondère les récompenses futures.
- **Température** : Paramètre de la méthode Softmax pour explorer ou exploiter les actions.

### Actions possibles

- **0** : Aller en haut
- **1** : Aller à droite
- **2** : Aller en bas
- **3** : Aller à gauche

### Génération de la courbe d'apprentissage

Le programme génère automatiquement une courbe des scores (lissée) représentant l'évolution des performances au fil des épisodes. Cette courbe est combinée avec une image de la carte pour une visualisation claire. Le fichier généré est nommé **map_with_curve.png** et se trouve dans le répertoire courant.



