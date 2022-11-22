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
from math import *
import sys






class Gift: # A verifier mais name doit etre unique en théorie
    def __init__(self, name:str, score:int, weight:int, target_c:int, target_r :int):
        self.name : str = name
        self.score : int = score
        self.weight : int = weight
        self.target_c : int = target_c
        self.target_r : int = target_r

    def __str__(self):
        return "Gift : ", self.name, " score : ", self.score, " weight : ", self.weight, " target_c : ", self.target_c, " target_r : ", self.target_r

class Santa: # Entité qui va etre mise a jour durant l'execution du programme pour verifier que tout est bon.
    # Le santa a des ordres absolus:
    # Donc pas de vérification dans ses méthodes. 
    # Mais modification des variables internes dépendantes des méthodes. si acceleration -> carrot--

    def __init__(self) :

        self.c : int = 0                                #Position en c ou X
        self.r : int = 0                                #Position en r ou Y

        self.vc : int = 0                               #Vitesse en c ou X
        self.vr : int = 0                               #Vitesse en r ou Y

        self.weight : int = 0                           #Poids du traineau
        self.carrots : int = 0                          #Nombres de carottes

        self.loadedGifts = {}              #loadedGifts Cadeau chargé liste


    def loadCarrots(self, nbCarrots : int) :
        self.carrots += nbCarrots
        self.weight += nbCarrots * 1 # une carotte pèse 1kg
    
    def loadGift(self, gift: Gift) :
        self.loadedGifts[gift.name] = gift
        self.weight += gift.weight

    def unLoadGift(self, gift_name: str) :
        gift = self.loadedGifts[gift_name] # TODO delete element from dict
        self.loadedGifts[gift_name] = None
        self.weight -= gift.weight
        return gift

    def updatePosition(self) : #s'active à chaque tours
        self.c += self.vc
        self.r += self.vr

    def getMaxAccelerationForCurrentWeight(self, weight_acceleration_ratio) -> int: #retourne l'acceleration max possible selon le tableau en constante globale en fonction du poids total du traineau. TODO Ajouter le typage valide
        for i in range(len(weight_acceleration_ratio)):
            if self.weight >= weight_acceleration_ratio[i][0]:
                return weight_acceleration_ratio[i][1]
        return weight_acceleration_ratio[len(weight_acceleration_ratio)-1][1] #return l'acceleration du dernier element de la liste. equivaut l'acceleration maximale possible qui est dans la liste

    # 4 fonction de changement d'acceleration
    def accUp(self, nb : int) : # accélération sur r Y
        self.vr += nb
        self.carrots -= 1 # lors d'une acceration, on consomme une carotte peut importe la force de l'acceleration
        self.weight -= 1
    
    def accDown(self, nb : int) : # deceleration sur r Y
        self.vr -= nb
        self.carrots -= 1 
        self.weight -= 1

    def accLeft(self, nb : int) : # acceleration sur c X
        self.vc -= nb
        self.carrots -= 1 
        self.weight -= 1

    def accRight(self, nb : int) : # deceleration sur c X
        self.vc += nb
        self.carrots -= 1 
        self.weight -= 1

    def Float(self, nb : int): # Met à jour le Santa nb fois
        for i in range(nb) :
            self.updatePosition()
    
            

    def toString(self) -> str:
        string = "SANTA : \n"
        string += "position c : " + str(self.c) + "\n"
        string += "position r : " + str(self.r) + "\n"
        string += "velocity c : " + str(self.vc) + "\n"
        string += "velocity r : " + str(self.vr) + "\n"
        string += "number of carrots : " + str(self.carrots) + "\n"
        string += "total weight : " + str(self.weight) + "\n"
        string += "gifts:\n"
        for gift in self.loadedGifts :
            string += "{gift.name} : {gift.score}pts, {gift.weight}kg, target_c={gift.target_c}, target_r={gift.target_r}\n"
        return string
        


if __name__ == "__main__":
    # # lire les arguments (challenge.txt,parcours.txt)
    # parser = argparse.ArgumentParser()
    # parser.add_argument("challenge", help="fichier de la situation de départ")
    # parser.add_argument("parcours", help="fichier du parcours généré")   
    # args = parser.parse_args()

    # # lire les fichiers
    # file_challenge = parser.parse_challenge(args.challenge)
    # file_parcours = parser.parse_parcours(args.parcours)

    # récupératino des arguments:
    file_path_challenge = sys.argv[1]
    file_path_parcours = sys.argv[2]

    # lecture des fichiers
    file_challenge = open(file_path_challenge, "r")
    file_parcours = open(file_path_parcours, "r")

    # RECUPERATION DES PARAMETRES DE LA SIMULATION
    #Parametres constants apres la lecture du challenge.
    max_time_sec:int = 0
    delivery_distance:int = 0
    acceleration_range:int = 0
    number_of_gifts:int = 0
    weight_acceleration_ratio = [] #couples des accelerations en fonction du poids total du traineau. TODO : list[tuple[int,int]] = []
    gifts = {} # TODO typage : list[Gift]

    # creation d'un santa
    santa = Santa()

    # Variables 
    delivered_gifts = {} # : list[Gift]  liste de cadeaux livrés. A la fin de la simulation on compte les scores des gifts de l'array pour déterminé le score total.
    float_counter: int = 0 # Le temps d'execution en secondes. Incrémentée à chaque Float et vérifiée régulièrement. 
    acceleration_this_turn: bool = False # si True, vérrouille la possibilité d'accelerer à nouveau durant le tour.

    print("Challenge")
    for i, line in enumerate(file_challenge): # basé sur solution stack overflow : https://stackoverflow.com/questions/2081836/how-to-read-specific-lines-from-a-file-by-line-number
        if i == 0:
            line_splitted = line.split("\n")[0].split(" ")
            max_time_sec = int(line_splitted[0])
            delivery_distance = int(line_splitted[1])
            acceleration_range = int(line_splitted[2])
            number_of_gifts = int(line_splitted[3])
            print(max_time_sec, delivery_distance, acceleration_range, number_of_gifts)

        if  0 < i and i <= acceleration_range:
            line_splitted = line.split(" ")
            print((int(line_splitted[0]), int(line_splitted[1])))
            weight_acceleration_ratio.append((int(line_splitted[0]), int(line_splitted[1]))) # weight, acceleration
           
        if i > acceleration_range:
            line_splitted = line.split("\n")[0].split(" ")
            gift = Gift(line_splitted[0], int(line_splitted[1]), int(line_splitted[2]), int(line_splitted[3]), int(line_splitted[4]))
            print(gift.name, gift.score, gift.weight, gift.target_c, gift.target_r)
            gifts[line_splitted[0]] = gift # name, score, weight, target_c, target_r
            
    print(gifts)

    print()
    print("Parcours")
    

    for i, line in enumerate(file_parcours):
        if i == 0:
            print(int(line))
            # Regle 1 : La première ligne indique le nombre de ligne dans le fichier sans compter la première ligne.
            num_lines = sum(1 for line in file_parcours)
            if num_lines != int(line)+1: # TODO vérifier comment connaitre le nombre de ligne d'un fichier
                raise Exception("Erreur ligne 0 : Le fichier parcours ne contient pas le nombre de lignes indiqué")
        
        if line == "" or line == "\n":
            raise Exception("Erreur ligne "+str(i)+" : La ligne est vide")
        
        # OPERATIONS:
        instruction = line.split("\n")[0].split(" ")[0]
        # LoadSomething:
        if instruction == "LoadCarrots" or instruction == "LoadGift" :
            #coordonnées du point de chargement:
            chargement_c = 0 
            chargement_r = 0
            
            if sqrt(abs(santa.c - chargement_c)**2 + abs(santa.r - chargement_r)**2) > delivery_distance:
                raise Exception("Erreur ligne "+str(i)+" : Le pere noel ne peut pas charger de cadeaux ou de carottes s'il n'est pas aux coordonnées 0,0")
            else:
                if instruction == "LoadCarrots":
                    santa.loadCarrots(int(line.split(" ")[1]))
                    print("loadCarrots",int(line.split("\n")[0].split(" ")[1]), " -> total carrots", santa.carrots)
                elif instruction == "LoadGift":
                    gift_name = line.split("\n")[0].split(" ")[1]
                    gift: Gift = gifts[gift_name] 
                    santa.loadGift(gift) # on prend le gift correspond dans notre dictionnaire de gifts et on le charge dans le santa avec la méthode (methode qui ajoute aussi le poid)
                    print("LoadGift", gift_name, " -> total weight", santa.weight)
        #DeliverGift
        if instruction == "DeliverGift":
            # verif si cadeau chargé
            gift_name = line.split("\n")[0].split(" ")[1]
            print("DeliverGift", gift_name)
            if gift_name not in santa.loadedGifts:
                raise Exception("Erreur ligne "+str(i)+". Le pere noel n'a pas chargé le cadeau de", gift_name)

            gift = santa.loadedGifts[gift_name]

            #vérif si coordonnées dans la range minimal
            if sqrt(abs(santa.c - gift.target_c)**2 + abs(santa.r - gift.target_r)**2) < delivery_distance:
                raise Exception("Erreur ligne "+str(i)+" : Le pere noel ne peut pas déposer le cadeau",gift_name,"car il n'est pas dans la zone de livraison.")
            else:
                delivered_gifts[gift_name] = santa.unLoadGift(gift_name) # on déplace le cadeau du traineau vers la liste des cadeaux livré. On compteras plus tard les score des cadeaux dans cette liste.

        # Acceleration:
        if instruction == "AccRight" or instruction == "AccLeft" or instruction == "AccUp" or instruction == "AccDown":
            
            if acceleration_this_turn == True: # A ton deja acceléré ce tour ?
                raise Exception("Erreur ligne "+str(i)+" : Le pere noel ne peut pas accélérer plus d'une fois par tour")
            
            maxAcceleration = santa.getMaxAccelerationForCurrentWeight(weight_acceleration_ratio) # Quel accceleration max peut on effectuer ?
            acc = int(line.split(" ")[1])
            if acc > maxAcceleration: # Tente on d'accelerer plus que autorisé ?
                raise Exception("Erreur ligne "+str(i)+". Acceleration "+str(acc)+"m/s² trop forte ! Max autorisé "+str(maxAcceleration)+"m/s² pour "+str(santa.weight)+"kg.") 
            
            if instruction == "AccRight":
                santa.accRight(acc)
                print("AccRight",acc)
            elif instruction == "AccLeft":
                santa.accLeft(acc)
                print("AccLeft",acc)
            elif instruction == "AccUp":
                santa.accUp(acc)
                print("AccUp",acc)
            elif instruction == "AccDown":
                santa.accDown(acc)
                print("AccDown",acc)
                
            acceleration_this_turn = True # changement d'état. Le pere noel ne pourra plus accelerer jusqu'au prochain Float.

        # Float
        if instruction == "Float":
            att = int(line.split(" ")[1])
            if att > 1:
                raise Exception("Avertissement ligne "+str(i)+". Attente superieur à 1s : "+str(att)+"s. Etes vous sur de perdre du temps sans rien faire ?")
            santa.Float(att)
            print("Float", att)
            float_counter += att
            acceleration_this_turn = False # on a floatté, donc on pourra accélérer à nouveau

        # Depassemeent de temps
        if float_counter > max_time_sec:
            raise Exception("Erreur ligne "+str(i)+". Le temps de jeu max est dépassé. Ecoulé : "+str(att)+"s. Max : "+str(max_time_sec))

    print()
    # Calcul score:
    total_score = 0
    for gift_name, gift in delivered_gifts.items():
        total_score += gift.score
    print("Score total :", total_score)


