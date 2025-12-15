# BE_M1_IDIM_2025-2026

## Objectif du projet
Ce dépôt contient le travail réalisé dans le cadre du BE du M1 IDIM.
Il vise à modéliser et visualiser la trajectoire d’une particule à travers
différentes zones physiques.


## Description des fichiers

### `trajectoire.py`
Ce fichier contient les fonctions de calcul de la trajectoire :
- définition des paramètres géométriques des différentes zones
- calcul des positions et vitesses dans chaque zone
- fonction de tracé des trajectoires et des limites physiques

Il constitue le **cœur physique / mathématique** du projet.


### `interface_graphique.py`
Ce fichier implémente une interface graphique permettant :
- de modifier les paramètres physiques (énergie, tensions, activation des zones)
- de lancer le calcul de trajectoire
- d’afficher graphiquement les résultats

Il sert d’**interface utilisateur** entre le modèle et l’utilisateur.


## Utilisation

```bash
python interface_graphique.py
