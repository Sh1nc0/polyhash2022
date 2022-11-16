#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Santa:

    def __init__(self) :
        self.vx : int = 0
        self.vy : int = 0
        self.weight : int = 0
        # self.dictV : ?
        self.carrots : int = 0
        self.loadedGifts : dict[int, int] = {}

    def getDistance(self, dv) -> float :
        pass

    def getMaxAcc(self) -> int:
        pass

    def setVx(self, newVx : int) :
        self.vx = newVx

    def setVy(self, newVy : int) :
        self.vy = newVy

    def setWeight(self, newWeight : int) :
        self.weight = newWeight
