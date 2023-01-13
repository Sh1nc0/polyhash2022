#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from objects.gift import Gift
from math import sqrt


class Santa:
    """
    Santa object
        This object represents Santa

    Attributes
    ----------
    x : int
        X coordinate of Santa

    vx : int
        X velocity of Santa

    y : int
        Y coordinate of Santa

    vy : int
        Y velocity of Santa

    weight : int
        Weight of Santa

    maxSpeed : list[tuple[int, int]]
        List of tuples (weight, maxSpeed) used to compute the maximum speed of Santa

    carrots : int
        Number of carrots

    loadedGifts : list[Gift]
        List of gifts loaded by Santa
    """

    def __init__(self):
        """
        Parameters
        ----------
        x : int
            X coordinate of Santa

        vx : int
            X velocity of Santa

        y : int
            Y coordinate of Santa

        vy : int
            Y velocity of Santa

        weight : int
            Weight of Santa

        maxSpeed : list[tuple[int, int]]
            List of tuples (weight, maxSpeed) used to compute the maximum speed of Santa

        carrots : int
            Number of carrots

        loadedGifts : list[Gift]
            List of gifts loaded by Santa
        """

        self.x: int = 0
        self.vx: int = 0

        self.y: int = 0
        self.vy: int = 0

        self.weight: int = 0
        self.maxSpeed: list[tuple[int, int]] = []
        self.carrots: int = 0

        self.loadedGifts: list[Gift] = []

    def getDistance(self, x, y) -> float:
        """
        Get the distance between the santa and the point x, y

        Parameters
        ----------
        x : int
            X coordinate of the point

        y : int
            Y coordinate of the point

        Returns
        -------
        float
            Distance between the santa and the point x, y
        """
        return sqrt((self.x - x) ** 2 + (self.y - y) ** 2)

    def getMaxAcc(self) -> int:
        """
        Get the maximum acceleration of Santa

        Returns
        -------
        int
            Maximum acceleration of Santa
        """
        for v in self.maxSpeed:
            weight, speed = v
            if weight > self.weight:
                return speed

    def updatePosition(self):
        """
        Update the position of Santa
        """
        self.x += self.vx
        self.y += self.vy

    def findGift(self, name: str) -> int:
        """
        Find a gift in the list of loaded gifts

        Parameters
        ----------
        name : str
            Name of the gift

        Returns
        -------
        int
            Index of the gift in the list of loaded gifts

            -1 if not found
        """
        for i in range(len(self.loadedGifts)):
            if self.loadedGifts[i].name == name:
                return i
        return -1

    def getMaxWeight(self) -> int:
        """
        Get the maximum weight of Santa

        Returns
        -------
        int
            Maximum weight of Santa
        """
        return self.maxSpeed[-1][0]

    def __str__(self) -> str:
        """
        Returns
        -------
        str
            String representation of Santa
        """
        return f"x: {self.x} y: {self.y} vx: {self.vx} vy: {self.vy} w: {self.weight} c: {self.carrots}"
