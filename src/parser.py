#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from objects.deliveryPoint import DeliveryPoint
from objects.santa import Santa

class Parser:

    def __init__(self, filename: str):
        self.filename: str = filename

        self.time: int = 0
        self.deliveryDistance: int = 0
        self.nbAcc: int = 0
        self.nbGifts: int = 0

        self.santa: Santa = Santa()
        self.deliveryPoints: list = []

    def parse(self):
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
                    DeliveryPoint
                    properties[0]: Name
                    properties[1]: Score
                    properties[2]: Weight
                    properties[3]: X
                    properties[4]: Y
                """
                self.deliveryPoints.append(DeliveryPoint(properties[0], int(properties[1]), int(properties[2]), int(properties[3]), int(properties[4])))