from math import sqrt
from util.constants import *
from objects.game import Game
from objects.gift import Gift
from objects.santa import Santa

def finish(g: Game):
    if len(g.santa.loadedGifts) > 0 :
        g.santa.loadedGifts.sort(key=lambda x: g.santa.getDistance(x.x, x.y))
        for gift in g.santa.loadedGifts :
            if g.santa.getDistance(gift.x, gift.y) <= g.maxDeliveryDistance :
                g.deliverGift(gift)
    g.finish()
    print(f"score : {g.score}")
    exit()

def getDistXDistY(a:int, b:int, x:int, y:int):
    return x-a, y-b

def getDist(x0:int, y0:int, x1:int, y1:int):
    return sqrt((x1-x0)**2 + (y1-y0)**2)

def stopMoving(g : Game) :
    if g.santa.vx != 0 :
        if g.santa.vx > 0 :
            g.accelerate(g.santa.vx, ACCELERATE_LEFT)
        else :
            g.accelerate(-g.santa.vx, ACCELERATE_RIGHT)
        if g.timeCount+1 < g.timeLimit :
            g.floatX(1)
        else:
            finish(g)

    if g.santa.vy != 0 :
        if g.santa.vy > 0 :
            g.accelerate(g.santa.vy, ACCELERATE_DOWN)
        else :
            g.accelerate(-g.santa.vy, ACCELERATE_UP)
        if g.timeCount+1 < g.timeLimit :
            g.floatX(1)
        else:
            finish(g)

def goInRange(x : int, y : int, g : Game) :

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
            finish(g)

    print(f"{g.timeCount}/{g.timeLimit}    done x | actual pos {g.santa.x, g.santa.y}")

    stopMoving(g)
    if g.timeCount >= g.timeLimit :
        finish(g)


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
            finish(g)

    print(f"{g.timeCount}/{g.timeLimit}    done y")

    stopMoving(g)
    if g.timeCount >= g.timeLimit :
        finish(g)

def goTo(x : int, y : int, g : Game) :

    #Calculate the amount of carrots needed
    if g.santa.getDistance(0, 0) <= g.maxDeliveryDistance:
        carrots = (abs(g.santa.x - x)//g.santa.getMaxAcc() + abs(g.santa.y - y)//g.santa.getMaxAcc() + 2)*3
        print(f"Carrots needed : {carrots}")
        if g.santa.carrots < carrots:
            g.loadCarrots(carrots-g.santa.carrots)

    while g.santa.x != x:
        distX = abs(g.santa.x - x)
        print(f"{g.timeCount}/{g.timeLimit}        {g.santa.vx} {g.santa.x, g.santa.y}")

        if x > g.santa.x:
            mv = g.santa.getMaxAcc()
            print(mv)
            if distX < mv:
                if g.santa.vx > 0:
                    g.accelerate(abs(mv-distX), ACCELERATE_LEFT)
                elif g.santa.vx == 0:
                    g.accelerate(distX if distX < mv else mv, ACCELERATE_RIGHT)

                if g.timeCount+1 < g.timeLimit:
                    g.floatX(1)
                else:
                    finish(g)
                
                if g.santa.x >= x:
                    stopMoving(g)

            else:
                g.accelerate(mv, ACCELERATE_RIGHT)
                tf = distX//mv

                if g.timeCount+tf < g.timeLimit:
                    g.floatX(tf)
                else:
                    g.floatX(g.timeLimit-g.timeCount)
                    finish(g)

                if g.santa.x >= x:
                    stopMoving(g)
        else:
            mv = g.santa.getMaxAcc()
            if distX < mv:
                if g.santa.vx < 0:
                    g.accelerate(abs(mv-distX), ACCELERATE_RIGHT)
                elif g.santa.vx == 0:
                    g.accelerate(distX if distX < mv else mv, ACCELERATE_LEFT)

                if g.timeCount+1 < g.timeLimit:
                    g.floatX(1)
                else:
                    finish(g)
                if g.santa.y >= y:
                    stopMoving(g)
            else:
                g.accelerate(mv, ACCELERATE_LEFT)
                tf = distX//mv

                if g.timeCount+tf < g.timeLimit:
                    g.floatX(tf)
                else:
                    finish(g)

                if g.santa.x <= x:
                    stopMoving(g)

    print(f"{g.timeCount}/{g.timeLimit} done x {g.santa.vx} {g.santa.x, g.santa.y}")

    
    while g.santa.y != y:
        distY = abs(g.santa.y - y)
        print(f"{g.timeCount}/{g.timeLimit}        {g.santa.vy} {g.santa.x, g.santa.y}")

        if y > g.santa.y:
            mv = g.santa.getMaxAcc()
            if distY < mv:
                if g.santa.vy > 0:
                    g.accelerate(abs(mv-distY), ACCELERATE_DOWN)
                elif g.santa.vy == 0:
                    g.accelerate(distY if distY < mv else mv, ACCELERATE_UP)
                if g.timeCount+1 < g.timeLimit:
                    g.floatX(1)
                else:
                    finish(g)
                stopMoving(g)
            else:
                g.accelerate(mv, ACCELERATE_UP)
                tf = distY//mv

                if g.timeCount+tf < g.timeLimit:
                    g.floatX(tf)
                else:
                    g.floatX(g.timeLimit-g.timeCount)
                    finish(g)

                if g.santa.y > y:
                    stopMoving(g)
        else:
            mv = g.santa.getMaxAcc()
            if distY < mv:
                if g.santa.vy < 0:
                    g.accelerate(abs(mv-distY), ACCELERATE_UP)
                elif g.santa.vy == 0:
                    g.accelerate(distY if distY < mv else mv, ACCELERATE_DOWN)
                if g.timeCount+1 < g.timeLimit:
                    g.floatX(1)
                else:
                    finish(g)
                stopMoving(g)
            else:
                g.accelerate(mv, ACCELERATE_DOWN)
                tf = distY//mv

                if g.timeCount+tf < g.timeLimit:
                    g.floatX(tf)
                else:
                    g.floatX(g.timeLimit-g.timeCount)
                    finish(g)

                if g.santa.y < y:
                    stopMoving(g)

    print(f"{g.timeCount}/{g.timeLimit} done y {g.santa.vx} {g.santa.x, g.santa.y}")
    stopMoving(g)