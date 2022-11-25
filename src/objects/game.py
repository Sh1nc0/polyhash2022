#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from objects.santa import Santa
from objects.gift import Gift
from parser import Parser
import os

class Game :

    def __init__(self, p : Parser, output_dist: str = "../data/output_data/output.txt") :

        if p is None :
            raise Exception

        self.actionCount : int = 0
        self.maxDeliveryDistance : int = p.deliveryDistance
        
        self.timeLimit : int = p.time
        self.timeCount : int = 0

        self.score : int = 0

        self.santa : Santa = p.santa

        self.toDeliver : list[Gift] = p.gifts

        self.dist : str = output_dist
        self.outputString : list[str] = []

    def accelerate(self, nb : int, dir : str) :
        if dir.lower() == "up" :
            self.santa.vy += nb
            self.outputString.append(f"AccUp {nb}\n")
        elif dir.lower() == "down" :
            self.santa.vy -= nb
            self.outputString.append(f"AccDown {nb}\n")
        elif dir.lower() == "right" :
            self.santa.vx += nb
            self.outputString.append(f"AccRight {nb}\n")
        elif dir.lower() == "left" :
            self.santa.vx -= nb
            self.outputString.append(f"AccLeft {nb}\n")
        else :
            return

        self.santa.carrots -= 1
        self.santa.weight -= 1
        self.actionCount += 1


    def floatX(self, nb : int) :
        self.timeCount += nb

        self.outputString.append(f"Float {nb}\n")
        self.actionCount += 1

        for _ in nb :
            self.santa.updatePosition()

    def loadCarrots(self, nbCarrots : int) :
        self.santa.carrots += nbCarrots
        self.santa.weight += nbCarrots
        
        self.outputString.append(f"LoadCarrots {nbCarrots}\n")
        self.actionCount += 1

    def loadGift(self, g : Gift) :
        self.toDeliver.remove(g)
        self.santa.loadedGifts.append(g)
        self.santa.weight += g.weight

        self.outputString.append(f"LoadGift {g.name}\n")
        self.actionCount += 1

    def deliverGift(self, g : Gift) :
        self.santa.loadedGifts.remove(g)
        self.santa.weight -= g.weight

        self.outputString.append(f"DeliverGift {g.name}\n")
        self.actionCount += 1

    def finish(self) :
        os.makedirs(name=os.path.dirname(self.dist), exist_ok=True)
        with open(self.dist, 'w') as f :
            f.write(f"{self.actionCount}\n")
            
            for line in self.outputString:
                f.write(line)
        f.close()