# Pysize

Première version d'un outil en ligne de command python et qui permet de générer et d'enregistrer l'utilisation d'un disque dur.

Les données stockées sont:
- La date
- L'espace utilisé
- L'espace total
- Le type d'unité utilisé: Gb, Go, Mo, ...

On peut également exporter les résultat directement dans un fichier CSV.

## Utilisation
- Copier le fichier **sample-pysize-data.json** en **pysize-data.json**.
- Lancer le script: ```python3 pysize.py```

## Réduction de la taille du fichier
En Juin 2023, j'ai modifié le projet afin de rendre le fichier plus léger

| Nom                               | Nombre d'entrées | Taille       | Facteur de réduction                  | Modifications                                                |
| --------------------------------- | ---------------- | ------------ | ------------------------------------- | ------------------------------------------------------------ |
| Fichier v1 (oginal)               | **733**          | **159,4 Ko** | **0% **                               | Fichier original v1                                          |
| Fichier v2                        | **733**          | **99,4 Ko**  | **~48% ** (par rapport au fichier v1) | Indentation +  suppression des informations inutiles et réduction de la longueur du nom des clés. |
| Fichier v2-bis (sans indentation) | **733**          | **59,6 Ko**  | **~63% ** (par rapport au fichier v1) | Pas d'indentation: fichier sur une ligne +  suppression des informations inutiles et réduction de la longueur du nom des clés. |

J'ai retenu le fichier v2. Le fichier v2-bis est bien mais il est difficile de lire le JSON si on souhaites faire une modification.
