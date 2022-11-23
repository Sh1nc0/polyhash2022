#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from objects.santa import Santa
from objects.gift import Gift

class Game :

    def __init__(self) :
        self.actionCount : int = 0
        self.maxDeliveryDistance : int = 0
        
        self.timeLimit : int = 0
        self.timeCount : int = 0

        self.score : int = 0

        self.santa : Santa = None

        self.toDeliver : list[Gift] = []

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

    def loadGift(self, g : Gift) :
        self.toDeliver.remove(g)
        self.santa.loadedGifts.append(g)
        self.santa.weight += g.weight

        self.actionCount += 1

    def deliverGift(self, g : Gift) :
        self.santa.loadedGifts.remove(g)
        self.santa.weight -= g.weight

        self.actionCount += 1
