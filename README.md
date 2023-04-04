# gameslibrary

Premier test de Web App sous python avec Django.

L'objectif est de créer un gestionnaire de base de données qui permet:

1. D'importer sa liste de jeux (actuellement uniquement Steam et Playstation)
2. D'ajouter, de modifier ou de supprimer manuellement des jeux
3. De produire des dashboards: annuel et global


## Points d'attention:

En l'état, tout est configuré pour tourner avec une base de données locale Postgre.
Il est nécessaire de créer un projet Django puis de créer l'app GamesLibrary pour pouvoir utiliser les scripts.
Plusieurs librairies python supplémentaires ont été utilisées:
* Pour récupérer les infos PSN: PSNAWP
* Pour aller lire How Long To Beat: HowLongToBeat