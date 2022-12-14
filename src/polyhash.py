from objects.game import Game
from parser import Parser
from math import sqrt
import argparse

from util.constants import *

import time

def getDistXDistY(a:int, b:int, x:int, y:int):
    return x-a, y-b

def stopMoving(game : Game) :
    if g.santa.vx != 0 :
        if g.santa.vx > 0 :
            g.accelerate(g.santa.vx, ACCELERATE_LEFT)
        else :
            g.accelerate(-g.santa.vx, ACCELERATE_RIGHT)
        g.floatX(1)

    if g.santa.vy != 0 :
        if g.santa.vy > 0 :
            g.accelerate(g.santa.vy, ACCELERATE_DOWN)
        else :
            g.accelerate(-g.santa.vy, ACCELERATE_UP)
        g.floatX(1)

def goTo(x : int, y : int, game : Game) :

    inRange = g.santa.getDistance(x, y) <= g.maxDeliveryDistance

    print(f"{g.timeCount}/{g.timeLimit}    starting x | objective {x}")
    
    while (g.santa.x != x) and (not inRange) :

        print(f"{g.timeCount}/{g.timeLimit}        {g.santa.vx} {g.santa.x, g.santa.y}")
        if g.santa.vx == 0 :
            if g.santa.x < x :
                g.accelerate(1, ACCELERATE_RIGHT)
            else :
                g.accelerate(1, ACCELERATE_LEFT)
        g.floatX(1)

        inRange = g.santa.getDistance(x, y) <= g.maxDeliveryDistance

        if g.timeCount >= g.timeLimit :
            g.finish()
            exit()

    print(f"{g.timeCount}/{g.timeLimit}    done x | actual pos {g.santa.x, g.santa.y}")

    stopMoving(game)
    if g.timeCount >= g.timeLimit :
        g.finish()
        exit()

    print(f"{g.timeCount}/{g.timeLimit}    starting y | objective {y}")

    while (g.santa.y != y) and (not inRange) :

        print(f"{g.timeCount}/{g.timeLimit}        {g.santa.vy} {g.santa.y, g.santa.y}")

        if g.santa.vy == 0 :
            if g.santa.y < y :
                g.accelerate(1, ACCELERATE_UP)
            else :
                g.accelerate(1, ACCELERATE_DOWN)
        g.floatX(1)

        inRange = g.santa.getDistance(x, y) <= g.maxDeliveryDistance

        if g.timeCount >= g.timeLimit :
            g.finish()
            exit()

    print(f"{g.timeCount}/{g.timeLimit}    done y")

    stopMoving(game)
    if g.timeCount >= g.timeLimit :
            g.finish()
            exit()

if __name__ == "__main__":

    args = argparse.ArgumentParser(description='File Input')
    args.add_argument('fileInput', type=str, help='challenge definition filename', metavar="challenge.txt")
    args = args.parse_args()

    p = Parser(args.fileInput)
    p.parse()

    g = Game(p)
    g.toDeliver = sorted(g.toDeliver, key=lambda x : (abs(x.x) + abs(x.y)), reverse=True)

    for j in range(len(g.toDeliver)-1, -1, -1) :
        i = g.toDeliver[j]
        print(f"{g.timeCount}/{g.timeLimit} Gift : {i}")
        
        g.loadGift(i)
        g.loadCarrots(8 - g.santa.carrots)

        goTo(i.x, i.y, g)

        print(f"{g.timeCount}/{g.timeLimit} Voyage terminé : {i.x, i.y} | {g.santa.x, g.santa.y} {g.santa.vx, g.santa.vy}")

        g.deliverGift(i)

        if j != 0 :
            goTo(0, 0, g)

        print(f"{g.timeCount}/{g.timeLimit} Retour terminé : 0 0 | {g.santa.x, g.santa.y} {g.santa.vx, g.santa.vy}\n\n")

    g.finish()