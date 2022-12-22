from objects.game import Game
from parser import Parser
from math import sqrt
import argparse

from util.constants import *
from util.functions import *

if __name__ == "__main__":

    args = argparse.ArgumentParser(description='File Input')
    args.add_argument('fileInput', type=str, help='challenge definition filename', metavar="challenge.txt")
    args = args.parse_args()

    p = Parser(args.fileInput)
    #p = Parser("/Users/romain/Desktop/polyhash2022/data/input_data/f_festive_flyover.in.txt")
    p.parse()

    g = Game(p)
    
    t = [(0,0),(20,0),(-20,0),(0,20),(0,-20),(20,20), (-20,20), (20,-20), (-20,-20), (40,0), (-40,0), (0,40), (0,-40), (40,40), (-40,40), (40,-40), (-40,-40), (60,0), (-60,0), (0,60), (0,-60), (60,60), (-60,60), (60,-60), (-60,-60)]

    for i in range(len(t)):
        g.toDeliver.sort(key=lambda x: getDist(x.x, x.y,t[i][0], t[i][1]))
        goTo(0, 0, g)
        print(f"{g.santa.x} {g.santa.y}")

        for j in range(len(g.toDeliver)):
            if getDist(g.toDeliver[0].x, g.toDeliver[0].y, t[i][0], t[i][1])<= g.maxDeliveryDistance :
                g.loadGift(g.toDeliver[0])

        goTo(t[i][0], t[i][1], g)
        print(f"{g.santa.x} {g.santa.y}")
        for i in range(len(g.santa.loadedGifts)):
            g.deliverGift(g.santa.loadedGifts[0])


    finish(g)

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