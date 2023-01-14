# <u>Projet Poly#</u>

## <u>Contexte</u>

Ce travail a été réalisé dans le cadre d'un projet demandé par Polytech. Le sujet du défi est tiré de la finale du Google Hashcode 2022.

## <u>Fonctionnement du projet</u>

Description du fonctionnement du projet, notamment comment le lancer.

## <u>L'équipe</u>

- Membres :

Hippolyte ROUSSEL hippolyte.roussel@etu.univ-nantes.fr  
Romain PIPON romain.pipon@etu.univ-nantes.fr  
Lilian FORGET lilian.forget1@etu.univ-nantes.fr  
Leo BRIGARDIS leo.brigardis@etu.univ-nantes.fr

## <u>Procédure d'installation</u>

## <u>Procédure d'exécution</u>

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