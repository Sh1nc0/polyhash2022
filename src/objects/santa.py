#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from deliveryPoint import DeliveryPoint
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

        self.loadedGifts : list[DeliveryPoint] = []     #Cadeau chargé (représenté par leur Delivery Point)

    def getDistance(self, dv : DeliveryPoint) -> float :
        return abs(sqrt((self.x - dv.x) ** 2 + (self.y - dv.y) ** 2))

    def getMaxAcc(self) -> int:
        for v in self.maxSpeed :
            weight, speed = v
            if weight > self.weight :
                return speed
