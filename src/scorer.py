#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Hippolyte ROUSSEL hippolyte.roussel@etu.univ-nantes.fr
# 20/11/22
#
# Vérifie que les mouvements dans le fichier parcours_généré suivent les règles imposées du défi suivant une  situation_de_depart. Fournit un score si tout est bon ou lance des exceptions si une règle n'est pas respectée.
# Liste des règles : https://codingcompetitions.withgoogle.com/hashcode/round/00000000008cacc6/0000000000aff4a0 Section "Validation" (bas de page)
#
# INPUT:
# challenge.txt // fichier des cadeaux à transmettre
# parcours.txt // fichier des mouvements du pere-noel pour remettre les différents cadeaux.
# IMPORT interne au projet:
# parser.py // de Romain. Pour accéder aux données du challenge plus facilement.
# OUTPUT
# score:int || Exception d'une règle non respecté

# parcours.txt à la forme de l'exemple suivant: (sans les commentaires)
# 23
# LoadCarrots 10
# LoadGift Olivia
# LoadGift Liam
# AccRight 4
# Float 1
# DeliverGift Olivia
# AccUp 2
# Float 1
# DeliverGift Liam
# AccLeft 8
# Float 1
# AccDown 4
# Float 1
# LoadGift Bob
# AccRight 4
# Float 1
# AccDown 6
# Float 1
# AccDown 6
# Float 1
# AccDown 6
# Float 4
# DeliverGift Bob


import argparse
import math



#Parametres de la simulation. Constant apres la lecture du challenge.
max_time_sec = 0
delivery_distance = 0
acceleration_range = 0
number_of_gifts = 0
weight_acceleration_ratio = [] #couples des accelerations en fonction du poids total du traineau
gifts = []

# Variables 
delivered_gifts = [] # liste de cadeaux livrés. A la fin de la simulation on compte les scores des gifts de l'array pour déterminé le score total.
float_counter = 0 # Le temps d'execution en secondes. Incrémentée à chaque Float et vérifiée régulièrement. 
acceleration_this_turn = False # si True, vérrouille la possibilité d'accelerer à nouveau durant le tour.

class Gift: # A verifier mais name doit etre unique en théorie
    def __init__(self, name:str, score:int, weight:int, target_x:int, target_y :int):
        self.name = ""
        self.score = 0
        self.weight = 0
        self.target_x = 0
        self.target_y = 0

class Santa: # Entité qui va etre mise a jour durant l'execution du programme pour verifier que tout est bon.
    # Le santa a des ordres absolus:
    # Donc pas de vérification dans ses méthodes. 
    # Mais modification des variables internes dépendantes des méthodes. si acceleration -> carrot--

    def __init__(self) :

        self.x : int = 0                                #Position en X
        self.y : int = 0                                #Position en Y

        self.vx : int = 0                               #Vitesse en X
        self.vy : int = 0                               #Vitesse en Y

        self.weight : int = 0                           #Poids du traineau
        self.carrots : int = 0                          #Nombres de carottes

        self.loadedGifts : list[Gift] = []              #Cadeau chargé liste


    def loadCarrots(self, nbCarrots : int) :
        self.carrots += nbCarrots
        self.weight += nbCarrots * 1 # une carotte pèse 1kg
    
    def loadGift(self, gift: Gift) :
        self.loadedGifts.append(gift)
        self.weight += gift.weight

    def unLoadGift(self, gift_name: str) :
        gift = self.loadedGifts[gift_name] # TODO delete element from dict
        self.weight -= gift.weight
        return gift

    def updatePosition(self) : #s'active à chaque tours
        self.x += self.vx
        self.y += self.vy

    def getMaxAccelerationForCurrentWeight(self) -> int: #retourne l'acceleration max possible selon le tableau en constante globale en fonction du poids total du traineau
        for i in range(len(weight_acceleration_ratio)):
            if self.weight >= weight_acceleration_ratio[i][0]:
                return weight_acceleration_ratio[i][1]
        return weight_acceleration_ratio[len(weight_acceleration_ratio)-1][1] #return l'acceleration du dernier element de la liste. equivaut l'acceleration maximale possible qui est dans la liste

    # 4 fonction de changement d'acceleration
    def accUp(self, nb : int) : # accélération sur Y
        self.vy += nb
        self.carrots -= 1 # lors d'une acceration, on consomme une carotte peut importe la force de l'acceleration
        self.weight -= 1
    
    def accDown(self, nb : int) : # deceleration sur Y
        self.vy -= nb
        self.carrots -= 1 
        self.weight -= 1

    def accLeft(self, nb : int) : # acceleration sur X
        self.vx -= nb
        self.carrots -= 1 
        self.weight -= 1

    def accRight(self, nb : int) : # deceleration sur X
        self.vx += nb
        self.carrots -= 1 
        self.weight -= 1

    def Float(self, nb : int): # Met à jour le Santa nb fois
        for i in range(nb) :
            self.updateSpeed()
            self.updatePosition()
            self.float_counter += 1
    
            

    def toString(self) -> str:
        string = "SANTA : \n"
        string += "position x : " + str(self.x) + "\n"
        string += "position y : " + str(self.y) + "\n"
        string += "velocity x : " + str(self.vx) + "\n"
        string += "veloity y : " + str(self.vy) + "\n"
        string += "number of carrots : " + str(self.carrots) + "\n"
        string += "total weight : " + str(self.weight) + "\n"
        string += "gifts:\n
        for gift in self.loadedGifts :
            string += "{gift.name} : {gift.score}pts, {gift.weight}kg, target_x={gift.target_x}, target_y={gift.target_y}\n"
        return string
        


if __name__ == "__main__":
    # lire les arguments (challenge.txt,parcours.txt)
    parser = argparse.ArgumentParser()
    parser.add_argument("challenge", help="fichier de la situation de départ")
    parser.add_argument("parcours", help="fichier du parcours généré")   
    args = parser.parse_args()

    # lire les fichiers
    file_challenge = parser.parse_challenge(args.challenge)
    file_parcours = parser.parse_parcours(args.parcours)


    # RECUPERATION DES PARAMETRES DE LA SIMULATION

    #lis la premiere ligne du fichier challenge.txt
    challenge_first_line = file_challenge[0].split(" ")
    max_time_sec = int(challenge_first_line[0])
    delivery_distance = int(challenge_first_line[1])
    acceleration_range = int(challenge_first_line[2])
    number_of_gifts = int(challenge_first_line[3])

    #pour acceleration_range lignes suivantes, on lit les couples (max_weight, acceleration)
    for i in range(acceleration_range) :
        weight_acceleration_ratio.append(file_challenge[i+1].split(" "))
    weight_acceleration_ratio = reversed(weight_acceleration_ratio) #plus facile de gerer en partant du poids le plus lourd

    # pour les number_of_gifts lignes suivantes, on lit les gifts
    for i in range(number_of_gifts) :
        gift_data = file_challenge[i+acceleration_range+1].split(" ")
        gifts[gift_data[0]] = Gift(gift_data[0], int(gift_data[1]), int(gift_data[2]), int(gift_data[3]), int(gift_data[4])) # création de l'objet Gift à partir des infos. Ajout dans le dict par son nom unique.


    # creation d'un santa
    santa = Santa()


    # VERIFICATION DES REGLES

    # Regle 1 : La première ligne indique le nombre de ligne dans le fichier sans compter la première ligne.
    if len(file_parcours) != file_parcours[0]+1:
        raise Exception("Erreur ligne {0} : Le fichier parcours ne contient pas le nombre de lignes indiqué")
    
    # Parcours de toutes les lignes du fichier parcours.txt
    for i in range(len(file_parcours)):
        
        # Regle 2 : Pas de ligne vide dans le fichier file_parcours
        if file_parcours[i] == "":
            raise Exception("Erreur ligne {i} : La ligne est vide")

        # OPERATIONS
        # LoadCarrots
        if file_parcours[i].split(" ")[0] == "LoadCarrots":
            #vérifications de coordonnées:
            if sqrt(abs(santa.x)**2 + abs(santa.y)**2) > delivery_distance:
                raise Exception("Erreur ligne {i} : Le pere noel ne peut pas charger de cadeaux ou de carottes s'il n'est pas aux coordonnées 0,0")
            else:
                santa.loadCarrots(file_parcours[i].split(" ")[1])

        # LoadGift
        if file_parcours[i].split(" ")[0] == "LoadGift":
            #vérifications de coordonnées:
            if sqrt(abs(santa.x)**2 + abs(santa.y)**2) > delivery_distance:
                raise Exception("Erreur ligne {i} : Le pere noel ne peut pas charger de cadeaux ou de carottes s'il n'est pas aux coordonnées 0,0")
            else:
                santa.loadGift(gifts[file_parcours[i].split(" ")[1]]) # on prend le gift correspond dans notre dictionnaire de gifts et on le charge dans le santa

        #DeliverGift
        if file_parcours[i].split(" ")[0] == "DeliverGift":
            # verif si cadeau chargé
            if santa.gift[file_parcours[i].split(" ")[1]] is None:
                raise Exception("Erreur ligne {i}. Le pere noel n'a pas chargé ce cadeau")

            #vérif si coordonnées dans la range minimal
            if sqrt(abs(santa.x)**2 + abs(santa.y)**2) < delivery_distance:
                raise Exception("Erreur ligne {i} : Le pere noel ne peut pas déposer de cadeaux s'il n'est pas dans la zone de livraison.")
            else:
                delivered_gifts.append(santa.deliverGift(file_parcours[i].split(" ")[1])) # on déplace le cadeau du traineau vers la liste des cadeaux livré. On compteras plus tard les score des cadeaux dans cette liste.

        # Acceleration:
        instruction = file_parcours[i].split(" ")[0]
        if instruction == "AccRight" or instruction == "AccLeft" or instruction == "AccUp" or instruction == "AccDown":
            
            if acceleration_this_turn == True: # A ton deja acceléré ce tour ?
                raise Exception("Erreur ligne {i} : Le pere noel ne peut pas accélérer plus d'une fois par tour")
            
            maxAcceleration = santa.getMaxAccelerationForCurrentWeight() # Quel accceleration max peut il effectuer ?
            acc = file_parcours[i].split(" ")[1]
            if acc > maxAcceleration: # Tente on d'accelerer plus que autorisé ?
                raise Exception("Erreur ligne {i}. Acceleration {acc}m/s² trop forte ! Max autorisé {maxAcceleration}m/s² pour {self.weight}kg.") 
            
            match instruction:
                case "AccRight":
                    santa.accRight(acc)
                case "AccLeft":
                    santa.accLeft(acc)
                case "AccUp":
                    santa.accUp(acc)
                case "AccDown":
                    santa.accDown(acc)
                
            acceleration_this_turn = True # changement d'état. Le pere noel ne pourra plus accelerer jusqu'au prochain Float.

        # Float
        if file_parcours[i].split(" ")[0] == "Float":
            att = file_parcours[i].split(" ")[1]
            if att > 1:
                raise Exception("Avertissement ligne {i}. Attente superieur à 1 : {att}s. Etes vous sur de perdre du temps sans rien faire ?")
            santa.Float(att)
            float_counter += att
            acceleration_this_turn = False # on a flotté, donc on pourras accélérer à nouveau

        # Depassemeent de temps
        if float_counter > max_time_sec:
            raise Exception("Erreur ligne {i}. Le temps de jeu max est dépassé. Ecoulé : {att}s. Max : {max_time_sec}")

    # Calcul score:
    total_score:
    for gift in delivered_gifts:
        total += gift.score
    return total_score



