#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from objects.santa import Santa
from objects.gift import Gift
from util.constants import ACCELERATE_UP, ACCELERATE_DOWN, ACCELERATE_RIGHT, ACCELERATE_LEFT, LOAD_GIFT, LOAD_CARROTS, DELIVER_GIFT, FLOAT
from parser import Parser
import os
import time


class Game:

    def __init__(self, p: Parser):
        self.start_time = time.time()
        if p is None:
            raise Exception

        self.actionCount: int = 0
        self.maxDeliveryDistance: int = p.deliveryDistance

        self.timeLimit: int = p.time
        self.timeCount: int = 0

        self.score: int = 0

        self.santa: Santa = p.santa

        self.toDeliver: list[Gift] = p.gifts
        self.deliveredGifts: list[Gift] = []

        self.outputString: list[str] = []
        self.outDist: str = f"../data/output_data/{p.filename.split('/')[-1].replace('.in', '.out')}"

    def accelerate(self, nb: int, dir: str):
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
        self.timeCount += nb

        self.outputString.append(f"{FLOAT} {nb}\n")
        self.actionCount += 1

        for _ in range(nb):
            self.santa.updatePosition()

    def loadCarrots(self, nbCarrots: int):
        self.santa.carrots += nbCarrots
        self.santa.weight += nbCarrots

        self.outputString.append(f"{LOAD_CARROTS} {nbCarrots}\n")
        self.actionCount += 1

    def loadGift(self, g: Gift):
        self.toDeliver.remove(g)
        self.santa.loadedGifts.append(g)
        self.santa.weight += g.weight

        self.outputString.append(f"{LOAD_GIFT} {g.name}\n")
        self.actionCount += 1

    def deliverGift(self, g: Gift):
        self.deliveredGifts.append(g)
        self.santa.loadedGifts.remove(g)
        self.santa.weight -= g.weight
        self.score += g.score

        self.outputString.append(f"{DELIVER_GIFT} {g.name}\n")
        self.actionCount += 1

    def finish(self, outputDirectory: str = None):
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
        for i in range(len(self.toDeliver)):
            if self.toDeliver[i].name == name:
                return i
        return -1
