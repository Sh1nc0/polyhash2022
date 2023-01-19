#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Hippolyte ROUSSEL hippolyte.roussel@etu.univ-nantes.fr
# 10/12/22
#
# Class Autopilot : 
# permet de calculer  et connaitre différents paramètres utiles pour le pilotage du père Noel et permet de calculer les instructions à fournir au père Noel pour atteindre une cible.

import math
#from objects.Santa import Santa
#from objects.Gift import Gift


class Autopilot:

    # __init__(self):
    # def getDistanceToGift(self,santa:Santa,gift:Gift):
    #     return math.sqrt((gift.target_c - santa.position_c) ** 2 + (gift.target_r - santa.position_r) ** 2)

    # # Retourne un couple de 2 valeurs. Chacune sont la soustraction des coordonnées de la cible et du père Noel en C et R. (c equivalant à x, r à y)
    # def getRatioDirectionCR(self,santa:Santa,gift:Gift):
    #     return (gift.target_c - santa.position_c, gift.target_r - santa.position_r)

    # # Retourne un float correspondant au coefficient directeur de la droite reliant le père Noel à la cible. (c equivalant à x, r à y)
    # def getCoefDirecteurWithGift(self,santa:Santa,gift:Gift):
    #     return (gift.target_c - santa.position_c) / (gift.target_r - santa.position_r)

    # # Retourne le coefficient directeur de la droite reliant le père Noel à sa prochaine position (vecteur vitesse)
    # def convertSantaVectorToCoefDirecteur(self,santa:Santa):
    #     return santa.velocity_r / santa.velocity_c

    # # Retourne un angle en radians entre la droite du vecteur du père Noel et le vecteur de direction de la cible. 0 si le père Noel est deja sur la droite de la cible.
    # def getAngleDifferenceActualTarget(self,santa:Santa,gift:Gift):
    #     # coefficient directeur de la droite reliant le père Noel à la cible
    #     coefDirecteur = self.getCoefDirecteur(santa,gift)
    #     # coefficient directeur de la droite reliant le père Noel à sa prochaine position (vecteur vitesse)
    #     coefDirecteurSanta = self.convertSantaVectorToCoefDirecteur(santa)
    #     # angle entre les deux droites
    #     return math.atan((coefDirecteur - coefDirecteurSanta) / (1 + coefDirecteur * coefDirecteurSanta))

    # def calculNextHop(self,santa:Santa,gifts:list(Gift)):
        
    #     # si le vecteur velocity du Santa est de 0,0, on compare les distances entre le Santa et les gifts
    #     if santa.velocity_c == 0 and santa.velocity_r == 0:
    #         # on cherche le gift le plus proche
    #         minDistance = 100000000000000000
    #         nearestGift = None
    #         for gift in gifts:
    #             distance = self.getDistanceToGift(santa,gift)
    #             if distance < minDistance:
    #                 minDistance = distance
    #                 nearestGift = gift
    #         return nearestGift
        
    #     # Sinon on utilise getAngleDifferenceActualTarget pour tous les gifts pour connaitre celui avec l'angle le plus petit.
    #     minAngle = 100000000000000000
    #     nearestGift = None
    #     for gift in gifts:
    #         angle = self.getAngleDifferenceActualTarget(santa,gift)
    #         if angle < minAngle:
    #             minAngle = angle
    #             nearestGift = gift

    #     # On retourne le gift le plus proche.
    #     return nearestGift

    # # une fonction qui permet de décider si il vaut mieux aller tout droit et loin ou courber et proche comme prochain gift.
    
    # la methode initialement dans Santa.py mais vu que Santa.py n'est plus utilisé, je la mets ici.
    def getMaxAccelerationForCurrentWeight(self, weight_acceleration_ratios) -> int: # TODO typage : list[tuple[int,int]]
        for i in range(len(weight_acceleration_ratios)):                         # Pour chacun des couples(poids,accélération) de la liste
            if self.weight >= weight_acceleration_ratios[i][0]:                  # Si le poids du traineau est supérieur ou égal au poids du couple:
                return weight_acceleration_ratios[i][1]                          # On retourne l'accélération associée à ce couple
        return weight_acceleration_ratios[len(weight_acceleration_ratios)-1][1]   # Dans le cas ou le poids est plus petit que la limitation la plus faible (celle en fin de tableau), on retourne cette dernière limitation.
    
    
    # surcharge de la fonction addVectorGetInstructions
    # def addVectorGetInstructions(self,santa: Santa, TARGET_VELOCITY_C: int, TARGET_VELOCITY_R: int):
    #     MAX_ACC = self.getMaxAccelerationForCurrentWeight(santa.weight, santa.acceleration_ratios)
    #     self.addVectorGetInstructions(self,santa.position_c,santa.position_r,santa.velocity_c,santa.velocity_r,MAX_ACC, TARGET_VELOCITY_C,TARGET_VELOCITY_R)
    
    # On demande au père Noel d'accèlérer selon un vecteur de 2 dimensions. Les contraintes font qu'il ne peut accelerer que dans une seule direction chaque tour, et selon un maximum definit par sa masse.
    # Fourni une ou plusieurs listes d'instructions pour obtenir l'équivalent à ce vecteur, en un minimum de temps et d'espace. Le choix de quel manoeuvre à appliquer revient à l'utilisateur. Souhaite t il privilégier la consommation de carrot, le temps écoulé, ou veut une position très précise.
    def addVectorGetInstructions(self,INITIAL_POSITION_C: int,INITIAL_POSITION_R: int,INITIAL_VELOCITY_C: int,INITIAL_VELOCITY_R: int,MAX_ACC: int,TARGET_VELOCITY_C: int,TARGET_VELOCITY_R: int):

        # SYNCHRONISATION X
        # Situation : Le Santa se déplace suivant un vecteur actual_velocity_X ('X' car on ne tient pas compte de savoir si c'est en C ou R. On traite pour l'instant 1 dimension) et on veut atteindre un vecteur TARGET_VELOCITY_X.
        # Cependant, on ne peut pas accélérer de plus que MAX_ACC. On doit donc accélérer de MAX_ACC (ou moins) à chaque float.
        # initial_position_X = position du Santa au début de la manoeuvre.
        # Objectif: On cherche à atteindre TARGET_VELOCITY_X au moment ou Santa se trouve sur un multiple de TARGET_VELOCITY_X de sa position initiale. 
        # ex: si Santa est à la position 0 et que TARGET_VELOCITY_X = 10, on veut atteindre TARGET_VELOCITY_X au moment ou Santa est à la position 10, 20, 30, 40, etc.
        # Pour cela, on va accélérer à chaque float jusqu'à ce que Santa atteigne TARGET_VELOCITY_X - [un nombre entre 1 et MAX_ACC].
        # On va ensuite attendre un float, et accélérer une dernière fois pour atteindre TARGET_VELOCITY_X.
        # Ainsi, on sera synchronisé avec TARGET_VELOCITY_X.

        # SYNCHRONISATION Y
        # On peut repeter la meme chose sur l'axe Y. Mais pour etre toujours plus éfficace ont fera les 2 en meme temps et on vérifiera par une série de test lequel on manipule.

        # Cependant, effectuer les 2 manoeuvres simplement l'une après l'autre laissera écouler beaucoups trop de temps.
        # On cherche à minimiser le temps écoulé.
        # Pour cela on dispose de plusieurs outils:
        # Le premier est de déterminé quel est l'axe majeur (celui avec la plus grande différence entre actual_velocity_X et TARGET_VELOCITY_X).
        # En traitant le plus grand axe en premier, on se décalera moins de notre coefficient directeur cible (définit au début de la manoeuvre)
        # Le deuxieme outil est le point d'alternance.
        # Il permet de commencer à accelerer sur l'axe mineur rapidement avant le premier point de synchronisation et ainsi de se décaler le moins possible de notre axe cible (coef directeur) lorsqu'on continuera sur l'axe majeur.
        # Le point d'alternance se détermine comme étant INITIAL_POSITION_MAJORAXIS + math.floor(TARGET_VELOCITY_MAJORAXIS / TARGET_VELOCITY_MINORAXIS)
        # On obtient ainsi un point sur l'axe majeur qui est une fraction de TARGET_VELOCITY_MINORAXIS de l'axe majeur.
        # A moins que Santa soit sur un point de synchronisation et qu'il puisse terminer sa manoeuvre de l'axe majeur, le point d'alternance est prioritaire sur la poussée.
        # Le dernier outil à disposition est le facteur.
        # Il permet de repeter la manoeuvre plusieurs fois, et ainsi de réduire le temps écoulé. 
        # Il est le pgcd de TARGET_VELOCITY_X et TARGET_VELOCITY_Y.
        # On repetera la manoeuvre facteur fois.
        # Comme on répète la manoeuvre on répète aussi le point d'alternance au passage.

        instructions = []

        # On détermine l'axe majeur et nommons toutes nos variables en fonction de celui-ci.
        if abs(TARGET_VELOCITY_C) >= abs(TARGET_VELOCITY_R):
            MAJORAXIS = 'C'
            MINORAXIS = 'R'

            TARGET_VELOCITY_MAJORAXIS = TARGET_VELOCITY_C
            TARGET_VELOCITY_MINORAXIS = TARGET_VELOCITY_R
            INITIAL_POSITION_MAJORAXIS = INITIAL_POSITION_C
            INITIAL_POSITION_MINORAXIS = INITIAL_POSITION_R
        
            actual_velocity_majoraxis = INITIAL_VELOCITY_C
            actual_velocity_minoraxis = INITIAL_VELOCITY_R
            actual_position_majoraxis = INITIAL_POSITION_C
            actual_position_minoraxis = INITIAL_POSITION_R
        else:
            MAJORAXIS = 'R'
            MINORAXIS = 'C'

            TARGET_VELOCITY_MAJORAXIS = TARGET_VELOCITY_R
            TARGET_VELOCITY_MINORAXIS = TARGET_VELOCITY_C
            INITIAL_POSITION_MAJORAXIS = INITIAL_POSITION_R
            INITIAL_POSITION_MINORAXIS = INITIAL_POSITION_C
            
            actual_velocity_majoraxis = INITIAL_VELOCITY_R
            actual_velocity_minoraxis = INITIAL_VELOCITY_C
            actual_position_majoraxis = INITIAL_POSITION_R
            actual_position_minoraxis = INITIAL_POSITION_C


        # Sous fonction pour réobtenir les directions
        def convertAxisToInstructionDir(axis:str,velocity:int) -> str:
            print("converstion",axis,velocity)
            if axis == 'C':
                if velocity >= 0:
                    return "Right"
                else:
                    return "Left"
            elif axis == 'R':
                if velocity >= 0:
                    return "Up"
                else:
                    return "Down"
            else:
                raise Exception("Unsupported axis must be 'C' or 'R', got {axis}")


        def divisors(num1:int ,num2:int): #  -> list(int)
            xlist:list(int) = []
            for i in range(math.gcd(num1,num2)):
                if i != 0 and num1 % i == 0 and num2 % i == 0:
                    xlist.append(i)
            return xlist


        


        # On détermine le facteur. Puisqu'on cherche à minimiser le temps et non pas l'espace, on divise le moins possible pour toujours faire des grosses accélérations.
        best_factor = 1
        divs = divisors(TARGET_VELOCITY_MAJORAXIS,TARGET_VELOCITY_MINORAXIS)
        for i in range(len(divs)):
            if TARGET_VELOCITY_MAJORAXIS / divs[i] < MAX_ACC or TARGET_VELOCITY_MINORAXIS / divs[i] < MAX_ACC:
                if i == 0:
                    best_factor = 1
                else:
                    best_factor = divs[i-1]
                break
        factor = best_factor
        print("factor",factor)
        # factor = math.gcd(TARGET_VELOCITY_MAJORAXIS,TARGET_VELOCITY_MINORAXIS)

        # on détermine les constantes diminuées par le facteur
        TARGET_VELOCITY_MAJORAXIS_FACTOR = TARGET_VELOCITY_MAJORAXIS / factor
        TARGET_VELOCITY_MINORAXIS_FACTOR = TARGET_VELOCITY_MINORAXIS / factor
        

        # On détermine le point d'alternance
        alternance_point = 0 # dans le cas ou l'on aurait dej
        if TARGET_VELOCITY_MINORAXIS_FACTOR != 0:
            alternance_point = INITIAL_POSITION_MAJORAXIS + math.floor(TARGET_VELOCITY_MAJORAXIS_FACTOR / TARGET_VELOCITY_MINORAXIS_FACTOR)

        float_count = 0
        min_float_calculated =TARGET_VELOCITY_MAJORAXIS/MAX_ACC+1 +TARGET_VELOCITY_MINORAXIS/MAX_ACC+1 # on ne pourra jamais faire la manoeuvre en moins de ce nombre de mouvements. Car on ne peut faire que les c et r indépendamment et on ne peut pas aller plus vite que le MAX_ACC. Si on optient une valeur inferieur c'est qu'il y a forcément un problème


        def isOnSyncPoint() -> bool:
            return actual_position_majoraxis % TARGET_VELOCITY_MAJORAXIS_FACTOR == 0 

        def isOnePushable() -> bool:
            return abs(TARGET_VELOCITY_MAJORAXIS_FACTOR - actual_velocity_majoraxis) <= MAX_ACC

        # Pour chaque facteur, on effectue la manoeuvre
        for i in range(factor):

            isSyncMajorAxis = False
            isSyncMinorAxis = False
            
            alternance_point_check: bool = False
            
            while (actual_velocity_majoraxis != TARGET_VELOCITY_MAJORAXIS_FACTOR) or (actual_velocity_minoraxis != TARGET_VELOCITY_MINORAXIS_FACTOR) or (actual_position_minoraxis != INITIAL_POSITION_MINORAXIS + TARGET_VELOCITY_MINORAXIS_FACTOR*float_count):
                
                # affichage des actuals
                print()
                print("actual_position_majoraxis",actual_position_majoraxis)
                print("actual_position_minoraxis",actual_position_minoraxis)
                print("actual_velocity_majoraxis",actual_velocity_majoraxis)
                print("actual_velocity_minoraxis",actual_velocity_minoraxis)
                print("float_count",float_count)

                # Si on peut synchroniser sur l'axe majeur, on le fait
                if (not isSyncMajorAxis 
                and isOnSyncPoint()
                and isOnePushable()
                and actual_velocity_majoraxis != TARGET_VELOCITY_MAJORAXIS_FACTOR): # dernier critère pour éviter de synchroniser en faisant +0
                    # santa.accelerate(abs(TARGET_VELOCITY_MAJORAXIS_FACTOR - actual_velocity_majoraxis), self.convertAxisToInstructionDir(MAJORAXIS, TARGET_VELOCITY_MAJORAXIS_FACTOR - actual_velocity_majoraxis))
                    instruction = "accelerate" + str(convertAxisToInstructionDir(MAJORAXIS, TARGET_VELOCITY_MAJORAXIS_FACTOR - actual_velocity_majoraxis)) + " : " + str(abs(TARGET_VELOCITY_MAJORAXIS_FACTOR - actual_velocity_majoraxis)) + ""
                    instructions.append(instruction)
                    print('Synchronisation sur l\'axe majeur')
                    print(instruction)
                    actual_velocity_majoraxis += TARGET_VELOCITY_MAJORAXIS_FACTOR - actual_velocity_majoraxis
                    isSyncMajorAxis = True

                # Si on peut synchroniser sur l'axe mineur, on le fait.
                # Normalement il sera le deuxième à être synchronisé donc on vérifie si il est bien sur la trajectoire demandée
                elif (not isSyncMinorAxis # si pas déjà synchronisé
                and actual_position_minoraxis % (TARGET_VELOCITY_MINORAXIS_FACTOR * factor) == 0 # si on est sur un point de synchronisation
                and actual_position_minoraxis == TARGET_VELOCITY_MINORAXIS_FACTOR*(float_count) # si ce point de synchronisation est bien sur la trajectoire demandée
                and abs(TARGET_VELOCITY_MINORAXIS_FACTOR - actual_velocity_minoraxis) <= MAX_ACC # si on peut atteindre la vitesse demandée par une poussée
                and actual_velocity_minoraxis != TARGET_VELOCITY_MINORAXIS_FACTOR): # dernier critère pour éviter de synchroniser en faisant +0
                    
                    # santa.accelerate(abs(TARGET_VELOCITY_MINORAXIS_FACTOR - actual_velocity_minoraxis), self.convertAxisToInstructionDir(MINORAXIS, TARGET_VELOCITY_MINORAXIS_FACTOR - actual_velocity_minoraxis))
                    instruction = "accelerate" + str(convertAxisToInstructionDir(MINORAXIS, TARGET_VELOCITY_MINORAXIS_FACTOR - actual_velocity_minoraxis)) + " : " + str(abs(TARGET_VELOCITY_MINORAXIS_FACTOR - actual_velocity_minoraxis)) + ""
                    instructions.append(instruction)
                    print('Synchronisation sur l\'axe mineur')
                    print(instruction)
                    actual_velocity_minoraxis += TARGET_VELOCITY_MINORAXIS_FACTOR - actual_velocity_minoraxis   
                    isSyncMinorAxis = True                 




                # Si on à dépassé le point d'alternance
                elif (not alternance_point_check 
                and actual_position_majoraxis >= alternance_point):
                    alternance_point_check = True # TODO déterminer si il faut mettre plusieurs points d'alternance pour les ratios avec des pgcd tres grands. La boucle facteur permet déjà de répéter l'alternance plusieurs fois.
                    
                    power = 1 # TODO déterminer quelle est la puissance de poussée au point d'alternance. Est-ce toujours 1 ou MAX_ACC ou autre ?
                    instruction = "accelerate" + str(convertAxisToInstructionDir(MINORAXIS, TARGET_VELOCITY_MINORAXIS_FACTOR - actual_velocity_minoraxis)) + " : " + str(abs(power)) + ""
                    instructions.append(instruction) 
                    print('Poussée d\'alternance sur l\'axe mineur')
                    print(instruction)
                    actual_velocity_minoraxis += power 







                # Si on peut accélérer sur l'axe majeur, on le fait
                elif (not isSyncMajorAxis 
                # and TARGET_VELOCITY_MAJORAXIS_FACTOR - actual_velocity_majoraxis <= MAX_ACC
                and actual_velocity_majoraxis is not TARGET_VELOCITY_MAJORAXIS_FACTOR):

                    # Determine, via un pgcd(target_velo,actual_velo), la poussée qui permet de faire tomber le plus rapidement possible sur un sync_point. Puisqu'on cherche en objectif secondaire à minimiser l'espace perdu, autant vérifier.
                    # Ainsi si 2 poussées moindre permettent de tomber sur un sync_point, on le fait au lieu de pousser fort d'attenre plus longtemps pour un sync_point.
                    best_acc = 0
                    min_hop = 100000000000000
                    for i in range(0-MAX_ACC,MAX_ACC+1):
                        nb_hop = math.gcd(int(TARGET_VELOCITY_MAJORAXIS_FACTOR), int(actual_velocity_majoraxis + i))
                        if actual_velocity_majoraxis + i == 0: # gcd avec 0 retourne 0. On 
                            continue
                        if nb_hop <= min_hop:
                            min_hop = nb_hop
                            best_acc = i

                    instruction = "accelerate" + str(convertAxisToInstructionDir(MAJORAXIS, best_acc)) + " : " + str(abs(best_acc)) + ""
                    instructions.append(instruction)
                    actual_velocity_majoraxis += best_acc
                
                
                # elif (not isSyncMinorAxis 
                # and isSyncMajorAxis
                # and actual_velocity_minoraxis is not TARGET_VELOCITY_MINORAXIS_FACTOR):



                # Si on peut accélérer sur l'axe mineur, on le fait.
                # On pousse de manière à avoir une vitesse superieur pour rattraper l'axe visé, mais une vitesse qui reste reductible à TARGET_VELOCITY_MINORAXIS_FACTOR par une poussée MAX_ACC (qui se synchronisera par freinage)
                elif (not isSyncMinorAxis 
                and not TARGET_VELOCITY_MINORAXIS_FACTOR + MAX_ACC <= actual_velocity_minoraxis <= TARGET_VELOCITY_MINORAXIS_FACTOR + MAX_ACC # tant qu'on est pas dans la plage de vitesse où on peut freiner
                and not TARGET_VELOCITY_MINORAXIS_FACTOR * float_count - MAX_ACC <= actual_position_minoraxis <= TARGET_VELOCITY_MINORAXIS_FACTOR * float_count - MAX_ACC): # tant qu'on est pas dans la zone presque stable, on accélère
                    # Determine via un pgcd(target_velo,actual_velo) la poussée qui permet de faire tomber le plus rapidement possible sur un sync_point. Puisqu'on cherche en objectif secondaire à minimiser l'espace perdu, autant vérifier.
                    best_acc = 0
                    min_hop = 100000000000000
                    for i in range(0-MAX_ACC,MAX_ACC+1):
                        nb_hop = math.gcd(int(TARGET_VELOCITY_MINORAXIS_FACTOR*float_count), actual_velocity_minoraxis + i) # Le plus grand diviseur commun une fois qu'on aura poussée de i
                        if actual_velocity_minoraxis + i == 0: # gcd avec 0 retourne 0. On 
                            continue
                        if nb_hop < min_hop:
                            min_hop = nb_hop
                            best_acc = i

                    instruction = "accelerate" + str(convertAxisToInstructionDir(MINORAXIS, best_acc)) + " : " + str(abs(best_acc)) + ""
                    instructions.append(instruction)
                    actual_velocity_minoraxis += best_acc

                # Sinon on attend.
                # elif not isSyncMinorAxis and actual_position_minoraxis < TARGET_VELOCITY_MINORAXIS_FACTOR*float_count:
                #     instruction = "accelerate" + str(convertAxisToInstructionDir(MINORAXIS, TARGET_VELOCITY_MINORAXIS_FACTOR - actual_velocity_minoraxis)) + " : " + str(abs(TARGET_VELOCITY_MINORAXIS_FACTOR - actual_velocity_minoraxis)) + ""
                #     instructions.append(instruction)
                #     print('Poussée sur l\'axe mineur')
                #     if (TARGET_VELOCITY_MINORAXIS_FACTOR*float_count - actual_position_minoraxis) != 0:
                #         actual_velocity_minoraxis += 1
                #     else:
                #         actual_velocity_minoraxis += TARGET_VELOCITY_MINORAXIS_FACTOR - actual_velocity_minoraxis

                # Dans les autres cas, on attend. Il n'y a rien d'optimisable. Dans les tours suivants, on devrait atteindre un sync_point sur un des 2 axes.

                # On attend un tour
                actual_position_majoraxis += actual_velocity_majoraxis
                actual_position_minoraxis += actual_velocity_minoraxis
                instruction = "Float : 1"
                instructions.append(instruction)
                print(instruction)
                float_count += 1

                if float_count > 20:
                    break


        print()
        print("actual_position_majoraxis",actual_position_majoraxis)
        print("actual_position_minoraxis",actual_position_minoraxis)
        print("actual_velocity_majoraxis",actual_velocity_majoraxis)
        print("actual_velocity_minoraxis",actual_velocity_minoraxis)
        print("float_count",float_count)

        # Verfications:
        print()
        print(instructions)

        # Pas la bonne velocité
        if MAJORAXIS == 'C'and (actual_velocity_majoraxis != TARGET_VELOCITY_C or actual_velocity_minoraxis != TARGET_VELOCITY_R):
                raise Exception("Erreur dans les instructions. Le santa n'a pas la velocité attendue.")
        elif actual_velocity_majoraxis != TARGET_VELOCITY_R or actual_velocity_minoraxis != TARGET_VELOCITY_C:
                raise Exception("Erreur dans les instructions. Le santa n'a pas la velocité attendue.")
        
        # Pas sur l'axe:
        if (actual_position_majoraxis - INITIAL_POSITION_MAJORAXIS) / (actual_position_minoraxis - INITIAL_POSITION_MINORAXIS) != (actual_velocity_majoraxis - INITIAL_POSITION_MAJORAXIS) / (actual_velocity_minoraxis - INITIAL_POSITION_MINORAXIS):
            raise Exception("Erreur dans les instructions. Le santa n'est pas sur l'axe attendu.")

        if float_count < min_float_calculated:
            raise Exception("Erreur dans les instructions. Le nombre de est inferieur au minimum calculé")
        return instructions

    
# TESTS
if __name__ == "__main__":

    # Test 1
    init_pos_c = 0
    init_pos_r = 0
    init_velo_c = 0
    init_velo_r = 0
    max_acc = 1
    target_velo_c = 2
    target_velo_r = 2


    
    print("Test 1")
    auto = Autopilot()
    print("Santa props:")
    print("initial_position: {0}, {1}".format(init_pos_c, init_pos_r))
    print("initial_velocity: {0}, {1}".format(init_velo_c, init_velo_r))
    print("MAX_ACC: {0}".format(max_acc))
    print("Vecteur cible: {0}, {1}".format(target_velo_c, target_velo_r))
    print("Résultat:")
    print()
    auto.addVectorGetInstructions(init_pos_c, init_pos_r, init_velo_c, init_velo_r, max_acc, target_velo_c, target_velo_r)
    print()
