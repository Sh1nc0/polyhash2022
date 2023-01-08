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

def goTo(x: int, y: int, g: Game):

    distX = abs(g.santa.x - x)
    distY = abs(g.santa.y - y)

    if distX > g.santa.getMaxAcc(): 
        x1 = int(abs(g.santa.x - x)/2)
        if g.santa.x < x :
            while g.santa.x < x1:
                if g.santa.x + g.santa.vx + g.santa.getMaxAcc() > x1 :
                    break

                if g.timeCount + 1 >= g.timeLimit:
                    finish(g)

                g.accelerate(g.santa.getMaxAcc(), ACCELERATE_RIGHT)
                g.floatX(1)

            while g.santa.vx > 0:
                if g.timeCount + 1 >= g.timeLimit:
                    finish(g)

                g.accelerate(g.santa.getMaxAcc(), ACCELERATE_LEFT)
                g.floatX(1)

        elif g.santa.x > x :
            while g.santa.x > x1:
                if g.santa.x + g.santa.vx - g.santa.getMaxAcc() < x1 :
                    break
                if g.timeCount + 1 >= g.timeLimit:
                    finish(g)
                g.accelerate(g.santa.getMaxAcc(), ACCELERATE_LEFT)
                g.floatX(1)
            while g.santa.vx < 0:
                if g.timeCount + 1 >= g.timeLimit:
                    finish(g)
                g.accelerate(g.santa.getMaxAcc(), ACCELERATE_RIGHT)
                g.floatX(1)

    if distY > g.santa.getMaxAcc():
        y1 = int(abs(g.santa.y - y)/2)
        if g.santa.y < y :
            while g.santa.y < y1:
                if g.santa.y + g.santa.vy + g.santa.getMaxAcc() > y1 :
                    break
                if g.timeCount + 1 >= g.timeLimit:
                    finish(g)
                g.accelerate(g.santa.getMaxAcc(), ACCELERATE_UP)
                g.floatX(1)

            while g.santa.vy > 0:
                g.accelerate(g.santa.getMaxAcc(), ACCELERATE_DOWN)
                g.floatX(1)

        elif g.santa.y > y :
            while g.santa.y > y1:
                if g.santa.y + g.santa.vy - g.santa.getMaxAcc() < y1 :
                    break
                if g.timeCount + 1 >= g.timeLimit:
                    finish(g)
                g.accelerate(g.santa.getMaxAcc(), ACCELERATE_DOWN)
                g.floatX(1)
            while g.santa.vy < 0:
                if g.timeCount + 1 >= g.timeLimit:
                    finish(g)
                g.accelerate(g.santa.getMaxAcc(), ACCELERATE_UP)
                g.floatX(1)
    
    while g.santa.x != x:
        distX = abs(g.santa.x - x)
        print(f"{g.timeCount}/{g.timeLimit}        {g.santa.vx} {g.santa.x, g.santa.y}")

        if x > g.santa.x:
            max_acc = g.santa.getMaxAcc()
            print(g.santa.getMaxAcc())
            if distX < max_acc:
                if g.santa.vx > 0:
                    g.accelerate(abs(max_acc-distX), ACCELERATE_LEFT)
                elif g.santa.vx == 0:
                    g.accelerate(distX if distX < max_acc else max_acc, ACCELERATE_RIGHT)

                if g.timeCount+1 < g.timeLimit:
                    g.floatX(1)
                else:
                    finish(g)
                
                if g.santa.x >= x:
                    stopMoving(g)

            else:
                g.accelerate(max_acc, ACCELERATE_RIGHT)
                tf = distX//max_acc

                if g.timeCount+tf < g.timeLimit:
                    g.floatX(tf)
                else:
                    g.floatX(g.timeLimit-g.timeCount)
                    finish(g)

                if g.santa.x >= x:
                    stopMoving(g)
        else:
            max_acc = g.santa.getMaxAcc()
            if distX < max_acc:
                if g.santa.vx < 0:
                    g.accelerate(abs(max_acc-distX), ACCELERATE_RIGHT)
                elif g.santa.vx == 0:
                    g.accelerate(distX if distX < max_acc else max_acc, ACCELERATE_LEFT)

                if g.timeCount+1 < g.timeLimit:
                    g.floatX(1)
                else:
                    finish(g)
                if g.santa.y >= y:
                    stopMoving(g)
            else:
                g.accelerate(max_acc, ACCELERATE_LEFT)
                tf = distX//max_acc

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
            max_acc = g.santa.getMaxAcc()
            if distY < max_acc:
                if g.santa.vy > 0:
                    g.accelerate(abs(max_acc-distY), ACCELERATE_DOWN)
                elif g.santa.vy == 0:
                    g.accelerate(distY if distY < max_acc else max_acc, ACCELERATE_UP)
                if g.timeCount+1 < g.timeLimit:
                    g.floatX(1)
                else:
                    finish(g)
                stopMoving(g)
            else:
                g.accelerate(max_acc, ACCELERATE_UP)
                tf = distY//max_acc

                if g.timeCount+tf < g.timeLimit:
                    g.floatX(tf)
                else:
                    g.floatX(g.timeLimit-g.timeCount)
                    finish(g)

                if g.santa.y > y:
                    stopMoving(g)
        else:
            max_acc = g.santa.getMaxAcc()
            if distY < max_acc:
                if g.santa.vy < 0:
                    g.accelerate(abs(max_acc-distY), ACCELERATE_UP)
                elif g.santa.vy == 0:
                    g.accelerate(distY if distY < max_acc else max_acc, ACCELERATE_DOWN)
                if g.timeCount+1 < g.timeLimit:
                    g.floatX(1)
                else:
                    finish(g)
                stopMoving(g)
            else:
                g.accelerate(max_acc, ACCELERATE_DOWN)
                tf = distY//max_acc

                if g.timeCount+tf < g.timeLimit:
                    g.floatX(tf)
                else:
                    g.floatX(g.timeLimit-g.timeCount)
                    finish(g)

                if g.santa.y < y:
                    stopMoving(g)

    print(f"{g.timeCount}/{g.timeLimit} done y {g.santa.vx} {g.santa.x, g.santa.y}")
    stopMoving(g)