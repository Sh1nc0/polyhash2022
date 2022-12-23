from objects.game import Game
from parser import Parser
from math import sqrt
import argparse

from util.constants import *
from util.functions import *

def getMap(g: Game):
    x = [gift.x for gift in g.toDeliver]
    y = [gift.y for gift in g.toDeliver]

    return min(x), max(x), min(y), max(y)

def getGiftsInArea(x, y, g: Game):
    gifts = []
    amount=0
    for gift in g.toDeliver:
        if getDist(x, y, gift.x, gift.y) <= g.maxDeliveryDistance:
            gifts.append(gift)
            amount+=1

    return gifts

if __name__ == "__main__":

    args = argparse.ArgumentParser(description='File Input')
    args.add_argument('fileInput', type=str, help='challenge definition filename', metavar="challenge.txt")
    args = args.parse_args()

    p = Parser(args.fileInput)
    #p = Parser("/Users/romain/Desktop/polyhash2022/data/input_data/f_festive_flyover.in.txt")
    p.parse()

    g = Game(p)

    t = []
    # for i in range(0, -250, -g.maxDeliveryDistance):
    #     t.append((0, i)) 
    #     t.append((i, 0))
    #     t.append((i, i))

    # for i in range(0, 250, g.maxDeliveryDistance):
    #     t.append((0, i)) 
    #     t.append((i, 0))
    #     t.append((i, i))

    mS = (-500, 500, -500, 500)
    #mS = getMap(g)
    print(mS)

    for i in range(mS[0], mS[1], g.maxDeliveryDistance if g.maxDeliveryDistance else 1):
        for j in range(mS[2], mS[3], g.maxDeliveryDistance if g.maxDeliveryDistance else 1):
            t.append((i, j))

    print("2nd Parts")
    p=[]
    for i in t:
        score=0
        for gift in g.toDeliver:
            if getDist(gift.x, gift.y, i[0], i[1]) <= g.maxDeliveryDistance:
                score+=gift.score
        if score>0:
            p.append((i[0],i[1],score))
            print(i[0],i[1],score)
    p = list(set(p))
    p.sort(key=lambda x: x[2]/(getDist(x[0], x[1], 0,0)+1), reverse=True)
    print(p)
    t=p
    print("3rd Parts")

    for i in range(len(t)):
        g.toDeliver.sort(key=lambda x: getDist(x.x, x.y,t[i][0], t[i][1]))
        goTo(0, 0, g)
        print(f"{g.santa.x} {g.santa.y}")

        if g.santa.getDistance(0, 0) <= g.maxDeliveryDistance:
            for j in range(len(g.toDeliver)):
                if getDist(g.toDeliver[0].x, g.toDeliver[0].y, t[i][0], t[i][1])<= g.maxDeliveryDistance :
                    g.loadGift(g.toDeliver[0])

        goTo(t[i][0], t[i][1], g)
        print(f"{g.santa.x} {g.santa.y} ")
        for i in range(len(g.santa.loadedGifts)):
            print(f"{g.santa.loadedGifts[0]}")
            if g.santa.getDistance(g.santa.loadedGifts[0].x, g.santa.loadedGifts[0].y) <= g.maxDeliveryDistance:
                g.deliverGift(g.santa.loadedGifts[0])
            else:
                g.santa.loadedGifts.remove(g.santa.loadedGifts[0])

    finish(g)

    g.finish()
    print(f"score : {g.score}")


    # posx,posy = 0,0

    # for i in range(150):
    #     g.toDeliver.sort(key=lambda x: getDist(x.x, x.y,(posx),(posy)))
    #     goTo(0, 0, g)
    #     g.loadCarrots(200)

    #     for i in range(len(g.toDeliver)):
    #         if getDist(g.toDeliver[0].x, g.toDeliver[0].y, posx, posy)<= g.maxDeliveryDistance :
    #             g.loadGift(g.toDeliver[0])

        
    #     for i in range(len(g.santa.loadedGifts)):
    #         goTo(g.santa.loadedGifts[0].x, g.santa.loadedGifts[0].y, g)
    #         g.deliverGift(g.santa.loadedGifts[0])

    #     posx -= 15
    #     posy += 5