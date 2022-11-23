#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from objects.gift import Gift
from math import sqrt

class Santa:

    def __init__(self) :
        self.x : int = 0                                #Position en X
        self.vx : int = 0                               #Vitesse en X

        self.y : int = 0                                #Position en Y
        self.vy : int = 0                               #Vitesse en Y

        self.weight : int = 0                           #Poids du traineau
        self.maxSpeed : list[tuple[int,int]] = []       #Palier de vitesse
        self.carrots : int = 0                          #Nombres de carottes

        self.loadedGifts : list[Gift] = []     #Cadeau chargé

    def getDistance(self, x, y) -> float :
        return sqrt((self.x - x) ** 2 + (self.y - y) ** 2)

    def getMaxAcc(self) -> int:
        for v in self.maxSpeed :
            weight, speed = v
            if weight > self.weight :
                return speed
    
    def updatePosition(self) :
        self.x += self.vx
        self.y += self.vy
