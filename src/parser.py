#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from objects.gift import Gift
from objects.santa import Santa


class Parser:
    """
    Parser object
        This object parses the input file

    Attributes
    ----------
    filename : str
        Name of the input file

    time : int
        Time of the simulation

    deliveryDistance : int
        Distance to deliver a gift

    nbAcc : int
        Number of acceleration steps

    nbGifts : int
        Number of gifts

    santa : Santa
        Santa object

    gifts : list[Gift]
        List of gifts
    """

    def __init__(self, filename: str):
        """
        Parameters
        ----------
        filename : str
            Name of the input file
        """

        self.filename: str = filename

        self.time: int = 0
        self.deliveryDistance: int = 0
        self.nbAcc: int = 0
        self.nbGifts: int = 0

        self.santa: Santa = Santa()
        self.gifts: list[Gift] = []

    def parse(self):
        """
        Parse the input file
        """
        with open(self.filename, "r") as f:
            lines = f.readlines()

        for line in lines:
            properties = line.split(" ")

            if len(properties) == 4:
                """
                    Configuration
                    properties[0]: time
                    properties[1]: delivery distance
                    properties[2]: number of acceleration steps
                    properties[3]: number of gifts
                """
                self.time = int(properties[0])
                self.deliveryDistance = int(properties[1])
                self.nbAcc = int(properties[2])
                self.nbGifts = int(properties[3])

            if len(properties) == 2:
                """
                    Acceleration steps
                    properties[0]: weight
                    properties[1]: max speed
                """
                self.santa.maxSpeed.append((int(properties[0]), int(properties[1])))

            if len(properties) == 5:
                """
                    Gift
                    properties[0]: Name
                    properties[1]: Score
                    properties[2]: Weight
                    properties[3]: X
                    properties[4]: Y
                """
                self.gifts.append(Gift(properties[0], int(properties[1]), int(properties[2]), int(properties[3]), int(properties[4])))