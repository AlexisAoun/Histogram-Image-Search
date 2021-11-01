# Histogram-Image-Search
Recherche d'images par similiraté de leurs histogrammes


# Comment utilisé (programme en développement)

## Rechercher une image par similarité 

Dans le fichier main.py,

- Modifer queryPath, mettre la location de l'image que vous souhaitez chercher (jpg ou png)

- Modifier databasePath, mettre la location du fichier contenant la base de donnée souhaitée pour la recherche (jpg ou png)

- (optionel) Modifier numpyPath avec la location et le nom (.npy) de la sauvegarde numpy, si aucune sauvegarde une nouvelle sera créer avec le nom spécifier dans cette varialbe. Recommandé pour un chargement plus rapide

- Executer main.py

## Tester les algorithmes 

Pour pouvoir uniquement tester les algoritmes ACP et LSH :

- Mettre en commentaire toute la section recherche dans main.py

- Utiliser la fonction testCompletLsh de tests.py pour tester LSH

- Utiliser la fonction testACP de tests.py pour tester ACP


# Le programme est encore rudimentaire, le développment d'un gui et d'une cli plus développer est en cours 