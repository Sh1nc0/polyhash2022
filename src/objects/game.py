#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from objects.santa import Santa
from objects.deliveryPoint import DeliveryPoint

class Game :

    def __init__(self) :
        self.actionCount : int = 0
        self.maxDeliveryDistance : int = 0
        
        self.timeLimit : int = 0
        self.timeCount : int = 0

        self.score : int = 0

        self.santa : Santa = None

        self.toDeliver : list[DeliveryPoint] = []

    def accelerate(self, nb : int, dir : str) :
        if dir.lower() == "up" :
            self.santa.vx += nb
        elif dir.lower() == "down" :
            self.santa.vx -= nb
        elif dir.lower() == "right" :
            self.santa.vy += nb
        elif dir.lower() == "up" :
            self.santa.vy -= nb
        else :
            return

        self.santa.carrots -= 1
        self.santa.weight -= 1
        self.actionCount += 1


    def floatX(self, nb : int) :
        self.timeCount += nb
        self.actionCount += 1

        for _ in nb :
            self.santa.updatePosition()

    def loadCarrots(self, nbCarrots : int) :
        self.santa.carrots += nbCarrots
        self.santa.weight += nbCarrots
        
        self.actionCount += 1

    def loadGift(self, dv : DeliveryPoint) :
        self.toDeliver.remove(dv)
        self.santa.loadedGifts.append(dv)
        self.santa.weight += dv.weight

        self.actionCount += 1

    def deliverGift(self, dv : DeliveryPoint) :
        self.santa.loadedGifts.remove(dv)
        self.santa.weight -= dv.weight

        self.actionCount += 1
