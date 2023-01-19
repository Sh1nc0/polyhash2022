# Projet Polyhash Équipe R

## Table des matières

1. [Contexte](#contexte)
2. [Fonctionnement du projet](#fonctionnement-du-projet)
3. [L'équipe](#léquipe)
4. [Procédure d'installation](#procédure-dinstallation)
5. [Procédure d'exécution](#procédure-dexécution)
6. [Stratégie](#stratégie)
7. [Organisation du code](#organisation-du-code)
8. [Bugs et limitation connues](#bugs-et-limitation-connues)
9. [Autres](#autres)

## Contexte

Ce travail a été réalisé dans le cadre d'un projet demandé par Polytech. Le sujet du défi est tiré de la finale du Google Hashcode 2022.

## Fonctionnement du projet

Attention ! Le projet fonctionne sous python3.10, vous rencontrerez des erreurs si vous choississez de l'exécuter avec des versions précédentes.

- Lancement du projet :

```bash
$ cd src
$ python3 polyhash.py ../data/input_data/{'Nom du fichier'}.in.txt
```

Le score et le temps d'éxecution s'affiche dans le terminal et un fichier est crée appelé : {'Nom du fichier'}.out.txt

- Vérifier le fichier de sortie :

```bash
$ cd src
$ python3 scorer.py ../data/input_data/{'Nom du fichier'}.in.txt ../data/output_data/{'Nom du fichier'}.out.txt
```
Le score s'affiche dans le terminal. Il affiche également les erreurs si le fichier de sortie n'est pas valide.

## L'équipe

Hippolyte ROUSSEL hippolyte.roussel@etu.univ-nantes.fr  
Romain PIPON romain.pipon@etu.univ-nantes.fr  
Lilian FORGET lilian.forget1@etu.univ-nantes.fr  
Leo BRIGARDIS leo.brigardis@etu.univ-nantes.fr

## Stratégie

La stratégie mise en place consiste dans un premier temps d'analyser la carte et le positionnement des différents cadeaux. Ensuite le programme principal va déterminer quel algorithme convient le mieux. Chaque algorithme a sa propre stratégie.

### Algorithme 1: Cluster
Avec cet algorithme, nous avons décidé de regrouper les cadeaux en cluster. Pour cela nous avons utilisé l'algorithme de DBSCAN. Le père Noël va choisir le cluster le plus proche, charger les cadeaux et les carottes et s'y rendre. Une fois rendu au cluster il va décharger les cadeaux les plus proches de lui. Une fois fini il va revenir au point de départ et choisir le prochain cluster.

Une chose qui a été pensée mais pas implémenté est d'établir le meilleur chemin avec un algorithme de plus court chemin comme Kruskal ou Dijkstra.

### Algorithme 2: Max Delivery Distance

Avec cet algorithme, on découpe la map en différentes zones de taille égale à la Max Delivery Distance. Ensuite le père Noël choisit la zone la plus proche charge les cadeaux et les carottes et s'y rend. Une fois rendu à la zone il décharge les cadeaux tous les cadeaux et reviens au point de départ. Il choisit ensuite la prochaine zone la plus proche et recommence l'opération.

### Performance

| Map                   | A      | B     | C       | D       | E      | F       |
|-----------------------|--------|-------|---------|---------|--------|---------|
| Score                 | 0      |  0    | 150637  | 168845  | 63303  | 314131  |
| Temps d'éxecution (s) | 0.0006 |  2.88 |  25.23  |  5.27   | 33.8   |  6.33   |
| Mémoire (Mo)          | 8,3    |  9,6  |  13,2   |  11,9   | 13,1   |  12,6   |

Les scores ne correspondent pas tout à fait à ceux upload sur le site. Car il y eu certaines modifications pour améliorer la performance. 



## Organisation du code
```
.
|-- data                # Fichiers d'entrée et de sortie
|   |-- input_data 
|   |-- output_data
|   
|-- docs                # Documentation Doxygen
|-- recherches          
|-- hooks               # Hooks git, pour vérifier si les commits sont bien nommés
|-- src                 # Code source du projet
|   |-- objects
|   |   |-- game.py  
|   |   |-- gift.py
|   |   |-- santa.py
|   |
|   |-- util
|   |   |-- constants.py
|   |   |-- functions.py
|   |
|   |-- parser.py
|   |-- polyhash.py     # Fichier principal
|   |-- scorer.py       # Arbitre permet de vérifier la validité d'un fichier de sortie
| 
|-- tests
|   |-- Test.py        # Fichier de test principal 
|   |-- TestGame.py 
|   |-- TestParse.py
```


## Bugs et limitation connues

A ce jour, nous rencontrons des problèmes d'optimisation des déplacements. Notre santa n'accelère pas assez pour les points éloignés. Cela se ressent particulièrement sur la map B.

Aussi, le santa ne suit pas une courbe optimale vers sa destination ce qui le pousse à consommer plus de carotte que nécessaire.

## Autres

### Commits

Un point important et parfois sous estimé dans un projet et la gestion des commits ainsi que la clarté des noms de ces derniers.

#### Format de commit

Pour ces raisons, nous nous sommes mis d'accord dès le début du projet sur une convention de nommage. Aussi les "types" présent sur l'image ci-dessous serviront a créer des labels sur gitlab qui catégoriseront merge et issue.

![image](https://cdn.discordapp.com/attachments/765491179444764712/1039222782275375204/unknown.png)

#### Vérification des commits automatique

Enfin pour éviter toute erreur dans le nommage, nous avons ajouté un hooks qui intercepte les commits ne passant pas un regex. Pour l'utiliser :

A exécuté en local :
```
git config --local include.path ../.gitconfig
```

### Documentation

Ce projet utilise Doxygen afin de mettre en place une page statique de documentation généré depuis nos commentaires. Pour accéder à cette page : [Documentation](https://e203561m.univ-nantes.io/polyhash2022)