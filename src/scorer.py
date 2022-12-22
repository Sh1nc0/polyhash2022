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

# OUTPUT
# score:int || Exception d'une règle non respecté

import argparse
from math import *
from util.constants import *
from parser import Parser
from objects.gift import Gift
from objects.game import Game

if __name__ == "__main__":
    
    # récupération des arguments du programme:
    parser = argparse.ArgumentParser(description='Solve Poly# challenge.')

    parser.add_argument('challenge', type=str,
                        help='challenge definition filename', metavar="challenge.txt")
    parser.add_argument('parcours', type=str,
                        help='parcours definition filename', metavar="parcours.txt")

    args = parser.parse_args()

    # RECUPERATION DES PARAMETRES DE LA SIMULATION
    p = Parser(args.challenge)
    p.parse()
    g = Game(p)
 
    acceleration_this_turn: bool = False # si True, vérrouille la possibilité d'accelerer à nouveau durant le tour.

    with open(args.parcours, 'r') as file_parcours:
        lines = file_parcours.readlines()
        num_lines: int = len(lines)

    for i, line in enumerate(lines):

        if i == 0:
            print(int(line))
            # Regle 1 : La première ligne indique le nombre de ligne dans le fichier sans compter la première ligne.
            if num_lines != int(line)+1: # TODO vérifier comment connaitre le nombre de ligne d'un fichier
                raise Exception("Erreur ligne 0 : Le fichier parcours ne contient pas le nombre de lignes indiqué")
        
        if line == "" or line == "\n":
            raise Exception("Erreur ligne "+str(i)+" : La ligne est vide")
        
        # OPERATIONS:
        instruction: str = line.split()[0]
        
        # LoadSomething:
        if instruction == LOAD_CARROTS or instruction == LOAD_GIFT :
            #coordonnées du point de chargement:
            chargement_x: int = 0 
            chargement_y: int = 0
            
            if g.santa.getDistance(chargement_x, chargement_y) > g.maxDeliveryDistance:
                raise Exception("Erreur ligne "+str(i)+" : Le pere noel ne peut pas charger de cadeaux ou de carottes s'il n'est pas aux coordonnées 0,0")
           
            else:
                if instruction == LOAD_CARROTS:
                    nb: int = int(line.split()[1])
                    g.loadCarrots(nb)
                    print(LOAD_CARROTS,nb, " -> total carrots", g.santa.carrots)

                elif instruction == LOAD_GIFT:
                    gift_name = line.split()[1]
                    g.loadGift(g.toDeliver[g.findGiftIndex(gift_name)])
                    print(LOAD_GIFT, gift_name, " -> total weight", g.santa.weight)

        #DeliverGift
        if instruction == DELIVER_GIFT:
            # verif si cadeau chargé
            gift_name = line.split()[1]
            print(DELIVER_GIFT, gift_name)
            if g.santa.findGift(gift_name) == -1:
                raise Exception("Erreur ligne "+str(i)+". Le pere noel n'a pas chargé le cadeau de", gift_name)

            gift = g.santa.loadedGifts[g.santa.findGift(gift_name)]

            #vérif si coordonnées dans la range minimal
            if g.santa.getDistance(gift.x, gift.y) > g.maxDeliveryDistance:
                raise Exception("Erreur ligne "+str(i)+" : Le pere noel ne peut pas déposer le cadeau",gift_name,"car il n'est pas dans la zone de livraison.")
            else:
                g.deliverGift(gift)

        # Acceleration:
        if instruction == ACCELERATE_RIGHT or instruction == ACCELERATE_LEFT or instruction == ACCELERATE_UP or instruction == ACCELERATE_DOWN:
            
            if acceleration_this_turn == True: # A ton deja acceléré ce tour ?
                raise Exception("Erreur ligne "+str(i)+" : Le pere noel ne peut pas accélérer plus d'une fois par tour")
            
            maxAcceleration = g.santa.getMaxAcc() # Quel accceleration max peut on effectuer ?
            acc = int(line.split()[1])
            if acc > maxAcceleration: # Tente on d'accelerer plus que autorisé ?
                raise Exception("Erreur ligne "+str(i)+". Acceleration "+str(acc)+"m/s² trop forte ! Max autorisé "+str(maxAcceleration)+"m/s² pour "+str(g.santa.weight)+"kg.") 
            
            if instruction == ACCELERATE_RIGHT:
                g.accelerate(acc, ACCELERATE_RIGHT)
                print(ACCELERATE_RIGHT,acc)
            elif instruction == ACCELERATE_LEFT:
                g.accelerate(acc, ACCELERATE_LEFT)
                print(ACCELERATE_LEFT,acc)
            elif instruction == ACCELERATE_UP:
                g.accelerate(acc, ACCELERATE_UP)
                print(ACCELERATE_UP,acc)
            elif instruction == ACCELERATE_DOWN:
                g.accelerate(acc, ACCELERATE_DOWN)
                print(ACCELERATE_DOWN,acc)
                
            acceleration_this_turn = True # changement d'état. Le pere noel ne pourra plus accelerer jusqu'au prochain Float.

        # Float
        if instruction == FLOAT:
            att = int(line.split()[1])
            g.floatX(att)
            print(FLOAT, att)
            acceleration_this_turn = False # on a floatté, donc on pourra accélérer à nouveau

        # Depassemeent de temps
        if g.timeCount > g.timeLimit:
            raise Exception("Erreur ligne "+str(i)+". Le temps de jeu max est dépassé. Ecoulé : "+str(att)+"s. Max : "+str(g.timeLimit))

    # Calcul score:
    total_score = 0
    for gift in g.deliveredGifts:
        total_score += gift.score
    print("\nScore total :", total_score)


