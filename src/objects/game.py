#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from objects.santa import Santa
from objects.gift import Gift
from util.constants import ACCELERATE_UP, ACCELERATE_DOWN, ACCELERATE_RIGHT, ACCELERATE_LEFT, LOAD_GIFT, LOAD_CARROTS, DELIVER_GIFT, FLOAT
from parser import Parser
import os
import time

# Generate documentation with pydoc for doxygen


class Game:
    """
    Game object
        This object represents a game we use it to perform actions on Santa and to keep track of the game state

    Attributes
    ----------
    start_time : float
        Time at the start of the game used to compute the execution time

    actionCount : int
        Number of actions performed by Santa

    maxDeliveryDistance : int
        Maximum distance to deliver a gift

    timeLimit : int
        Time limit of the game

    timeCount : int
        Time elapsed

    score : int
        Score of the game

    santa : Santa
        Santa object

    toDeliver : list[Gift]
        List of gifts to deliver

    deliveredGifts : list[Gift]
        List of gifts delivered

    outputString : list[str]
        List of actions performed

    outDist : str
        Output file path
    """

    def __init__(self, p: Parser):
        if p is None:
            raise Exception

        self.start_time = time.time()
        self.actionCount: int = 0
        self.maxDeliveryDistance: int = p.deliveryDistance

        self.timeLimit: int = p.time
        self.timeCount: int = 0

        self.score: int = 0

        self.santa: Santa = p.santa

        self.toDeliver: list[Gift] = p.gifts
        self.deliveredGifts: list[Gift] = []

        self.outputString: list[str] = []
        self.outDist: str = f"../data/output_data/{p.filename.split('/')[-1].replace('.in', '.out')}"  # The default output directory is ../data/output_data/ + the name of the input file with the .in extension replaced by .out

    def accelerate(self, nb: int, dir: str):
        """
        Accelerate Santa
            Use this function to accelerate Santa in a given direction by a given number of units

        Parameters
        ----------
        nb : int
            Number of units to accelerate

        dir : str
            Direction to accelerate, can be ACCELERATE_UP, ACCELERATE_DOWN, ACCELERATE_RIGHT, ACCELERATE_LEFT refer to util/constants.py
        """

        if dir == ACCELERATE_UP:
            self.santa.vy += nb
            self.outputString.append(f"{ACCELERATE_UP} {nb}\n")
        elif dir == ACCELERATE_DOWN:
            self.santa.vy -= nb
            self.outputString.append(f"{ACCELERATE_DOWN} {nb}\n")
        elif dir == ACCELERATE_RIGHT:
            self.santa.vx += nb
            self.outputString.append(f"{ACCELERATE_RIGHT} {nb}\n")
        elif dir == ACCELERATE_LEFT:
            self.santa.vx -= nb
            self.outputString.append(f"{ACCELERATE_LEFT} {nb}\n")
        else:
            return

        self.santa.carrots -= 1
        self.santa.weight -= 1
        self.actionCount += 1

    def floatX(self, nb: int):
        """
        Float X units
            Update Santa's position and increment timeCount

        Parameters
        ----------
        nb : int
            Number of units to float
        """

        self.timeCount += nb

        self.outputString.append(f"{FLOAT} {nb}\n")
        self.actionCount += 1

        for _ in range(nb):
            self.santa.updatePosition()

    def loadCarrots(self, nbCarrots: int):
        """
        Load carrots on Santa to accelerate that increase Santa's weight

        Parameters
        ----------
        nbCarrots : int
            Number of carrots to load
        """

        self.santa.carrots += nbCarrots
        self.santa.weight += nbCarrots

        self.outputString.append(f"{LOAD_CARROTS} {nbCarrots}\n")
        self.actionCount += 1

    def loadGift(self, g: Gift):
        """
        Load a gift on Santa

        Parameters
        ----------
        g : Gift
            Gift to load
        """

        self.toDeliver.remove(g)
        self.santa.loadedGifts.append(g)
        self.santa.weight += g.weight

        self.outputString.append(f"{LOAD_GIFT} {g.name}\n")
        self.actionCount += 1

    def deliverGift(self, g: Gift):
        """
        Deliver a gift that is already loaded on Santa

        Parameters
        ----------
        g : Gift
            Gift to deliver
        """

        self.deliveredGifts.append(g)
        self.santa.loadedGifts.remove(g)
        self.santa.weight -= g.weight
        self.score += g.score

        self.outputString.append(f"{DELIVER_GIFT} {g.name}\n")
        self.actionCount += 1

    def finish(self, outputDirectory: str = None):
        """
        Finish the game and write the output file

        Parameters
        ----------
        outputDirectory : str
            Output file path
        """

        end_time = time.time()
        elapsed_time = end_time - self.start_time
        print('Execution time:', elapsed_time, 'seconds')

        os.makedirs(name=os.path.dirname(outputDirectory if outputDirectory is not None else str(self.outDist)), exist_ok=True)
        with open(outputDirectory if outputDirectory is not None else str(self.outDist), 'w') as f:
            f.write(f"{self.actionCount}\n")

            for line in self.outputString:
                f.write(line)
        f.close()

    def findGiftIndex(self, name: str) -> int:
        """
        Find the index of a gift in the toDeliver list

        Parameters
        ----------
        name : str
            Name of the gift

        Returns
        -------
        int
            Index of the gift in the toDeliver list

            -1 if not found
        """

        for i in range(len(self.toDeliver)):
            if self.toDeliver[i].name == name:
                return i
        return -1
