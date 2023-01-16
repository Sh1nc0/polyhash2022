# <u>Projet Poly#</u>

## <u>Contexte</u>

Ce travail a été réalisé dans le cadre d'un projet demandé par Polytech. Le sujet du défi est tiré de la finale du Google Hashcode 2022.

## <u>Fonctionnement du projet</u>

Attention ! Le projet fonctionne sous python3.10, vous rencontrerez des erreurs si vous choississez de l'exécuter avec des versions précédentes.

- Lancement du projet :

```bash
cd src
python3 polyhash.py ../data/input_data/{'Nom du fichier'}.in.txt
```

Le score s'affiche dans le terminal et un fichier est crée appelé : {'Nom du fichier'}.out.txt

## <u>L'équipe</u>

- Membres :

Hippolyte ROUSSEL hippolyte.roussel@etu.univ-nantes.fr  
Romain PIPON romain.pipon@etu.univ-nantes.fr  
Lilian FORGET lilian.forget1@etu.univ-nantes.fr  
Leo BRIGARDIS leo.brigardis@etu.univ-nantes.fr

## <u>Procédure d'installation</u>

## <u>Procédure d'exécution</u>

- Lancement du projet :

```bash
cd src
python3 polyhash.py ../data/input_data/{'Nom du fichier'}.in.txt
```

## <u>Stratégie</u>

## <u>Organisation du code</u>

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