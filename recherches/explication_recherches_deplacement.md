Hipoolyte ROUSSEL
17/01/2023

# Recherches Stratégies et Deplacements

## Stragtégies

J'ai aussi réfléchi à différentes trajectoires pour délivrer les cadeaux. J'en ai proposé plusieurs dont l'une ("Cluster") sera réutilisé dans le programme principal.

La première chose sur laquelle j'ai réfléchi était de définir quel était le trajet pseudo-optimal à suivre permettant de réduire les accélérations nécéssaire.

Pour ça j'ai commencé par trier mes cadeaux par un intéret. L'interet se calcul tel qu'étant un rapport entre le nombre de point que le cadeau rapporte, sa masse, et sa distance par rapport au centre.
J'obtenais ainsi une liste des cadeaux dans l'ordre par lequel il pourrait etre interessant de passer. Surtout si on les traites 1 par 1 dans un temps limité. (Stratégie "Line")

Ensuite je m'interesse à la trajectoire. J'ai établi plusieurs trajectoires correspondantes à différentes strétégies possibles.

<img src="https://lh5.googleusercontent.com/yuhnthmlM77-lvOwvkBK4s-mflVE6l8WmV_OnDWZZ65dBkYVwYyVCkJo-QSZ0_Rbs6g=w2400" alt="image strat_2_2.jpg from Google Drive" style="width:500px;"/>

<img src="https://lh3.googleusercontent.com/CV1fsS4Sdbf1q3NNLP9JL4BQ-NMe1M4vVpjWH9D68S0GN4r3xOxZX7KNl8DZmHnl61E=w2400" alt="image strat_1.jpg from Google Drive" style="width:500px;"/>

Je pense, sans pouvoir le démontrer, que le trajet hélice est celui qui est le plus éfficaces. Il permet de conserver un maximum de vitesse en passant sur les cadeaux. On peut déterminer les prochains cadeaux par lequels passer en calculant l'angle formé entre la trajectoire d'arrivée sur le premier cadeau et les trajectoires des suivants.

La statégie "Helix + first segment line variation" permet de déposer au passage sur le premier segment des cadeaux d'interet moindre qui se trouverais sur le chemin, sans dévier (ou très peu) de sa trajectoire.

Au final c'est la stratégie dite de "Cluster" qui sera mise en pratique avec une différence notable que les grands déplacements se font axe par axe au lieu de diagonal.

Pouvais-je trouver alors un moyen de générer une poussée diagonale de manière éfficace ? Sur les images on voit déjà quelques éléments qui annonce la partie suivante.

## Déplacements

Mon objectif était du coup de trouver une fonction permettant de convertir un vecteur bidimensionel en suite d'instructions qui correspondrait à appliquer ce vecteur.

N'étant pas devin j'ai commencé par chercher des points communs entre plusieurs situations qui me permettrai de comprendre et créer un algorithme.

### Schématisation

Pour ça je commence par la situation la plus simple: un vecteur de deplacement diagonale (1,1) avec une accélération maximale de 1 et une position et vitesse initiale de 0,0. Soit une situation de paramètres:
- TARGET_VELOCITY_C=1 (aka TVC ou VC ou C dans certaines images)
- TARGET_VELOCITY_R=1
- MAX_ACCELERATION=1
- INITIAL_POSITION_C=0 
- INITIAL_POSITION_R=0
- INITIAL_VELOCITY_C=0 (aka IVC ou VCI dans les images)
- INITIAL_VELOCITY_R=0

Avec des variables durant l'executions:
- actualVelocityC=0 (aka V00 pour le couple dans les images)
- actualVelocityC=0
- actualPositionC=0
- actualPositionR=0


<img src="https://lh6.googleusercontent.com/GjGHUQ-EiP-8NEVbOjXNs2IVP8RlUB8abHsqE5W0FuXimxmIYb8yojQEn-pcqXxFJS4=w2400" alt="image dep_VC2VR2M1_T4.jpg from Google Drive" style="width:500px;"/>

L'image représente la suite d'instruction optimale (en temps, en espace et en carburant) que notre Santa (représenté par un triangle) doit effectué:
- AccRight 1
- Float 1
- AccUp 1
- Float 1
- AccUp 1
- Float 1
- AccDown 1
- Float 1

On termine la manoeuvre après 4 float (t4). On arrive sur les coordonnées CR 4,4 (noté E4 ou E44 sur l'image)

_Toutes les imprécisions sur le nomage de certaines variables viennent du fait que j'ai commencé à tester sans connaitre toutes les variables dont j'allais avoir besoin. J'ai ajouté et modifier au fur et à mesure de mes recherches_

On voit que le float entre t1 et t2 nous mets sur un axe qui est décalé par rapport à là ou on devrait se trouver si on avait effectué AccRight 1 + AccUp 1 au meme moment.
L'objectif est donc de "remonter" sur l'axe visé. 

### Autres essais

<img src="https://lh5.googleusercontent.com/j5_p7VwxdXDgt_DFPNontb0-vQYsPOXs-hWc79EmErjjVJo5hAJjbUfs867BU-_KyV4=w2400" alt="image dep_VC2VR1M2_T4E43.jpg from Google Drive" style="width:300px;"/>

<img src="https://lh5.googleusercontent.com/1uz3mnJg8vudZzWJ8r58ZwZxfhTNwlYW8ym3wmQqZd762P9o6bflGh-7KNLYvAv1aso=w2400" alt="image dep_6_VC3VR2M1_T5E96.jpg from Google Drive" style="width:500px;"/>

Cette image est interressante car elle met en évidence que pour trouver deplacement optimal (en rouge) on ne peut pas juste effectuer toutes les poussées sur un axe puis toutes les poussées sur un autre (en bleu).
Il faut ALTERNER entre les poussées Right et Up pour s'éloigner à minima de l'axe visé.
On va donc chercher à optimiser nos poussées par ce que j'appelerais un "point d'alternance". C'est à dire un point qui une fois dessus (ou passé) éxigera une poussée sur l'autre axe.

Après plusieurs essais et différentes variantes. J'obtiens une idée de ce que je dois faire pour obtenir une suite d'instruction correcte dans toutes* les situations.

Je décris les étapes dans dep_7_
<img src="https://lh3.googleusercontent.com/lLlD-31eop8G2Miz6uxsB4lvvQUZz68m8o3J5Gaqk8DFuv6WEPcO-3l4EItZw23PBQ4=w2400" alt="image dep_7_algorithme.jpg from Google Drive" style="width:500px;"/>

<img src="https://lh6.googleusercontent.com/BzNlebUjw1tz3QcexHL-8HGQj4xl194ucIe5_q3qZTr14-uL9pHh7xxi39GNuxB9TAU=w2400" alt="image dep_9_position_arrivée.jpg from Google Drive" style="width:500px;"/>

La fonction fonctionne sur un principe de double synchronisation. On cherche à synchroniser la vitesse actuelle avec celle désirée mais seulement sur des multiples de notre vecteur voulu.
On effectue la meme synchronisation sur l'axe majeur (celui ayant la plus grande valeur) puis sur l'axe mineur.
Pour se synchroniser il faut avoir une vitesse courante inferieur ou égale de l'accélération maximale à notre vitesse voulu, au moment où l'on se trouve sur un multiple de notre vecteur. (point de synchronisation). Ainsi on peut accélérer un petit peut pour égaliser avec la vitesse voulu. Et ainsi on fera à chaque float, le bon "saut".



On cherche donc un point d'alternance sur lequel on fera une poussée sur l'axe mineure afin que notre trajectoire reste au plus pres de l'axe correspondant à notre vecteur. Cela permet d'avoir moins à rattraper une fois synchroniser sur l'axe majeur.
De plus on peut simplifier une manoeuvre importante comme C8R4 en trouvant le pgcd entre C et R. Ce qui donne 4 manoeuvre de C2R1.

Cependant on peut avoir des vecteur plus complexe ou il est impossible d'obtenir exactement un multiple de notre vecteur. 

<img src="https://lh5.googleusercontent.com/kjiuISGMvTP4lR5fskoZYeOU8-yjqk6N7U6Y6rCfsMx4tMVDsjDxqZ-3HA8ApYN0Dl0=w2400" alt="image dep_9_position_arrivée.jpg from Google Drive" style="width:500px;"/>

On à donc 3 fin possibles:
- La manoeuvre parfaite. Celle qu'on aurait du obtenir si on pouvait poussée sans limites de masse et sur 2 axes en meme temps. On peut l'obtenir pour des petites poussées uni-directionnelle comme le vecteur (1,0) par exemple.
- La manoeuvre presque parfaite. Celle qu'on obtient dans la majorité des cas. On a obtenu des points de synchronisations et poussées après plusieurs float en conséquences.
- La manoeuvre imparfaite. Celle qu'on pourrait obtenir si on force le fait de réduire la distance parcouru par la manoeuvre.

### Code


### Resultats

Cependant durant la programmation j'ai réaliser un problème majeur. Je me suis rendu compte que mon besoin avait été mal exprimé. Je n'avais pas clairement définit si je voulais additioner un vecteur à mon vitesse courante (par somme de vecteur) ou voulais-je juste indiquer un vecteur à suivre impérativement qui ajusterais la vitesse courante.
Dans les 2 cas la situation devenait trop complexe pour etre terminé dans les temps.






