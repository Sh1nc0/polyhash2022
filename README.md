# <u>Projet Poly#</u>

## <u>Table des matières</u>

1. [Contexte](#contexte)
2. [Fonctionnement du projet](#fonctionnement-du-projet)
3. [L'équipe](#léquipe)
4. [Procédure d'installation](#procédure-dinstallation)
5. [Procédure d'exécution](#procédure-dexécution)
6. [Stratégie](#stratégie)
7. [Organisation du code](#organisation-du-code)
8. [Bugs et limitation connues](#bugs-et-limitation-connues)
9. [Autres](#autres)

## <u>Contexte</u>

Ce travail a été réalisé dans le cadre d'un projet demandé par Polytech. Le sujet du défi est tiré de la finale du Google Hashcode 2022.

## <u>Fonctionnement du projet</u>

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

## <u>L'équipe</u>

Hippolyte ROUSSEL hippolyte.roussel@etu.univ-nantes.fr  
Romain PIPON romain.pipon@etu.univ-nantes.fr  
Lilian FORGET lilian.forget1@etu.univ-nantes.fr  
Leo BRIGARDIS leo.brigardis@etu.univ-nantes.fr

## <u>Procédure d'installation</u>

## <u>Procédure d'exécution</u>

- Lancement du projet :

```bash
$ cd src
$ python3 polyhash.py ../data/input_data/{'Nom du fichier'}.in.txt
```

## <u>Stratégie</u>

## <u>Organisation du code</u>
```
.
|-- data                # Fichiers d'entrée et de sortie
|   |-- input_data 
|   |-- output_data
|   
|-- docs                # Documentation Doxygen
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
|   |-- testGame.py 
|   |-- testParse.py
```


## <u>Bugs et limitation connues</u>

## <u>Autres</u>

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