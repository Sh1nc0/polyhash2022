



# Recherches Stratégies et Déplacements
Hipoolyte ROUSSEL
17/01/2023
## Stratégies


La première chose sur laquelle j'ai réfléchi était de définir quel était le trajet pseudo-optimal à suivre permettant de réduire les accélérations nécessaires.


Pour ça, j'ai commencé par trier mes cadeaux par intérêt. L'intérêt se calcule tel qu'étant un rapport entre le nombre de points que le cadeau rapporte, sa masse, le tout divisé par la distance du cadeau par rapport au centre.
J'obtenais ainsi une liste des cadeaux dans l'ordre par lequel il pourrait être intéressant de passer. (Surtout si on les traite selon une stratégie "Line")


Ensuite je m'intéresse à la trajectoire. J'ai établi plusieurs trajectoires correspondantes à différentes stratégies possibles.


<img src="https://lh5.googleusercontent.com/yuhnthmlM77-lvOwvkBK4s-mflVE6l8WmV_OnDWZZ65dBkYVwYyVCkJo-QSZ0_Rbs6g=w2400" alt="image strat_2_2.jpg from Google Drive" style="width:500px;"/>


<img src="https://lh3.googleusercontent.com/CV1fsS4Sdbf1q3NNLP9JL4BQ-NMe1M4vVpjWH9D68S0GN4r3xOxZX7KNl8DZmHnl61E=w2400" alt="image strat_1.jpg from Google Drive" style="width:500px;"/>


Je pense, sans pouvoir le démontrer, que la trajectoire hélice (milieu de page 2) est celle qui est le plus efficace. Elle permet de conserver un maximum de vitesse en passant sur les cadeaux. On peut déterminer les cadeaux suivants en calculant l'angle formé entre la ligne d'arrivée sur le premier cadeau et les lignes reliant ce cadeau aux  suivants.


La stratégie "Helix + first segment line variation" permet de déposer au passage sur le premier segment des cadeaux d'intérêt moindre qui se trouvera sur le chemin, sans dévier (ou très peu) de sa trajectoire.


Au final c'est la stratégie dite de "Cluster" qui sera mise en pratique avec une différence notable que les grands déplacements se font un axe après l'autre au lieu d’un déplacement diagonal.


Pouvais-je alors trouver un moyen de générer une poussée diagonale de manière efficace ?


## Déplacements


Mon objectif était du coup de trouver une fonction permettant de convertir un vecteur bidimensionnel en suite d'instructions qui correspondrait à appliquer ce vecteur.


Le problème évident est qu'en effectuant un float entre des poussées d’axes différents, on se retrouve sur un axe parallèle à notre objectif. Il faut donc pouvoir se réaligner.


N'étant pas devin j'ai commencé par chercher des points communs entre plusieurs situations qui me permettraient de comprendre et créer un algorithme.


### Schématisation


Pour ça je commence par la situation la plus simple: un vecteur de déplacement diagonale (1,1) avec une accélération maximale de 1 et une position et vitesse initiale de 0,0. Soit une situation de paramètres:
- TARGET_VELOCITY_C=1 (aka TVC ou VC ou C dans certaines images)
- TARGET_VELOCITY_R=1
- MAX_ACCELERATION=1
- INITIAL_POSITION_C=0
- INITIAL_POSITION_R=0
- INITIAL_VELOCITY_C=0 (aka IVC ou VCI dans les images)
- INITIAL_VELOCITY_R=0


Avec des variables durant l'exécutions:
- actualVelocityC=0 (aka V00 pour le couple dans les images)
- actualVelocityC=0
- actualPositionC=0
- actualPositionR=0


_Toutes les différences sur le nommage de certaines variables viennent du fait que j'ai commencé à tester sur papier sans connaître toutes les variables dont j'allais avoir besoin au final. Je les ai donc ajoutées et modifiées au fur et à mesure de mes recherches_


<img src="https://lh6.googleusercontent.com/GjGHUQ-EiP-8NEVbOjXNs2IVP8RlUB8abHsqE5W0FuXimxmIYb8yojQEn-pcqXxFJS4=w2400" alt="image dep_VC2VR2M1_T4.jpg from Google Drive" style="width:500px;"/>


L'image représente la suite d'instruction optimale (en temps, en espace et en carburant) que notre Santa (représenté par un triangle) doit effectuer:
- AccRight 1
- Float 1
- AccUp 1
- Float 1
- AccUp 1
- Float 1
- AccDown 1
- Float 1


On termine la manœuvre après 4 float (t4). On arrive sur les coordonnées (4,4) (parfois noté E4 ou E44 sur les images)


On voit que le float entre t1 et t2 nous met sur un axe qui est décalé par rapport à là ou on devrait se trouver si on avait effectué AccRight 1 + AccUp 1 au même moment.
L'objectif est donc de "remonter" sur l'axe visé.


### Autres essais


<img src="https://lh5.googleusercontent.com/j5_p7VwxdXDgt_DFPNontb0-vQYsPOXs-hWc79EmErjjVJo5hAJjbUfs867BU-_KyV4=w2400" alt="image dep_VC2VR1M2_T4E43.jpg from Google Drive" style="width:300px;"/>


<img src="https://lh6.googleusercontent.com/wG-UhcVzPNN1QAfCv7inDbpTS0fucYLOH0yR9ULeLm1AAl192q5MmswxoZ6iZKEjstw=w2400" alt="image dep_VC2VR1M2_T4E43.jpg from Google Drive" style="width:300px;"/>


<img src="https://lh3.googleusercontent.com/GYkyg4e_kt8vI9h41PJf0Nm5hBz-RXGgRFVeiu8qxCt3eGtIFjeIl3OFU7nk_joksAw=w2400" alt="image dep_VC2VR1M2_T4E43.jpg from Google Drive" style="width:500px;"/>




<img src="https://lh5.googleusercontent.com/1uz3mnJg8vudZzWJ8r58ZwZxfhTNwlYW8ym3wmQqZd762P9o6bflGh-7KNLYvAv1aso=w2400" alt="image dep_6_VC3VR2M1_T5E96.jpg from Google Drive" style="width:500px;"/>


Cette image est intéressante car elle met en évidence que pour trouver déplacement optimal (en rouge) on ne peut pas juste effectuer toutes les poussées sur un axe puis toutes les poussées sur un autre (en bleu).
Il faut ALTERNER entre les poussées Right et Up pour s'éloigner au minimum de l'axe visé.
On va donc chercher à optimiser nos poussées par ce que j'appellerais un "point d'alternance". C'est-à-dire un point qui, une fois dépassé, exigera une poussée sur l'autre axe.


### Alternance


On cherche donc un point d'alternance sur lequel on fera une poussée sur l'axe mineure afin que notre trajectoire reste au plus près de l'axe correspondant à notre vecteur. Cela permet d'avoir moins à rattraper une fois synchronisé sur l'axe majeur.
Le point d’alternance est défini comme étant la position correspondante à la fraction de l’axe majeur sur l’axe mineur arrondi à l'entier inférieur.
Si on veut un vecteur (3,2) alors il sera 3/2 de l,5 donc 1. Une fois 1 dépassé sur l’axe majeur, on accélèrera de 1 sur l’axe mineur.


### Facteur


La dernière astuce qui peut être utile est de simplifier un vecteur comme (8,4) en prenant le pgcd entre les 2 valeurs. Ce qui donne 4 manœuvres de vecteur (2,1).


### Algorithme


Après plusieurs essais et différentes variantes et ses éléments obtenus. J'obtiens une idée de ce que je dois faire pour obtenir une suite d'instruction correcte dans toutes* les situations.


<img src="https://lh3.googleusercontent.com/lLlD-31eop8G2Miz6uxsB4lvvQUZz68m8o3J5Gaqk8DFuv6WEPcO-3l4EItZw23PBQ4=w2400" alt="image dep_7_algorithme.jpg from Google Drive" style="width:500px;"/>



La fonction marche sur un principe de double synchronisation. On cherche à synchroniser la vitesse actuelle avec celle désirée en se positionnant sur des multiples de notre vecteur voulu.
Ex pour un vecteur (3,0), ce que je nomme les points de synchronisations sont 3,6,9,12,...
Si notre vitesse est légèrement inférieure ou légèrement supérieure, en effectuant une poussée entre 0 et l’accélération maximale, on peut atteindre notre vitesse désirée.
Le fait d’atteindre la vitesse désirée sur un multiple permet de simuler le fait d’avoir fait la bonne poussée sur 2 axes et d’avoir ensuite attendu.


On effectue le même principe de synchronisation sur l'axe majeur (la dimension du vecteur ayant la plus grande valeur) puis sur l'axe mineur.


Evidemment, on utilise le point d’alternance en attendant d’atteindre un point de synchronisation, pour ne pas trop dévier de notre axe désiré.


### Fin de manoeuvre

Cependant on peut avoir des vecteur plus complexes ou il est impossible d'obtenir exactement un multiple de notre vecteur.


<img src="https://lh5.googleusercontent.com/kjiuISGMvTP4lR5fskoZYeOU8-yjqk6N7U6Y6rCfsMx4tMVDsjDxqZ-3HA8ApYN0Dl0=w2400" alt="image dep_9_position_arrivée.jpg from Google Drive" style="width:500px;"/>

On à donc 3 fin de manoeuvre possibles:
- La manœuvre parfaite. Celle qu'on aurait dû obtenir si on pouvait pousser sans limites de masse et sur 2 axes en même temps. On peut l'obtenir pour des petites poussées uni-directionnelles comme le vecteur (1,0) par exemple.
- La manœuvre presque parfaite. Celle qu'on obtient dans la majorité des cas. On a obtenu des points de synchronisation et poussées après plusieurs floats en conséquence.
- La manœuvre imparfaite. Celle qu'on pourrait obtenir si on force le fait de réduire la distance parcourue par la manœuvre.


### Code

Pour le code j'ai combiné les 2 synchronisation dans une boucle while. A chaque tour on vérifie plusieurs conditions:
- "Puis je synchroniser l'axe majeur ?",
- "Puis je synchroniser l'axe mineur ?",
- "Ai-je dépasser le point d'alternance ?",
- "Ai-je velocity sur l'axe Majeur entre TV-MaxAcc < AV < TV ?",
- ...

Dans les autres cas on peut pousser sur un des 2 axes en cherchant à se synchroniser. A la fin on termine par un Float avant de continuer la boucle.

Bien que n’étant pas fonctionnel, le code est disponible dans son propre fichier.

L'objectif était de proposer une classe autopilot statique contenant plusieurs méthodes. La plus évidente est celle évoquée dans ce rapport mais j'envisageai à terme d'ajouter une méthode permettant à un point demandé, d'avoir une vitesse demandée. Puis une autre permettant à partir d'une liste de points de passage, la suite d'instruction complète.
Toutes ces fonctions permettants de faciliter les déplacements et donner de précieuses infos permettant de tester différentes stratégies.


### Résultats

Cependant durant la programmation j'ai réalisé un problème majeur. Je me suis rendu compte que mon besoin avait été mal exprimé. Je n'avais pas clairement défini si je voulais additionner un vecteur à ma vitesse courante (par somme de vecteur) ou voulais-je juste indiquer un vecteur à suivre impérativement qui ajuste la vitesse courante.
Dans les 2 cas la situation devenait trop complexe pour être terminée dans les temps.

## Annexe

Les autres photos de feuilles sont sur le drive :
https://drive.google.com/drive/folders/1RfS89iGrPY8g8fat6KZyjVqnnOHqg4iY?usp=sharing









