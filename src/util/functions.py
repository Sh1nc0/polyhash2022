from math import sqrt
from util.constants import ACCELERATE_UP, ACCELERATE_DOWN, ACCELERATE_RIGHT, ACCELERATE_LEFT
from objects.game import Game


def finish(g: Game):
    if len(g.santa.loadedGifts) > 0:
        g.santa.loadedGifts.sort(key=lambda x: g.santa.getDistance(x.x, x.y))
        for gift in g.santa.loadedGifts:
            if g.santa.getDistance(gift.x, gift.y) <= g.maxDeliveryDistance:
                g.deliverGift(gift)
    g.finish()
    print(f"score: {g.score}")
    exit()


def getDist(x0: int, y0: int, x1: int, y1: int):
    return sqrt((x1 - x0)**2 + (y1 - y0)**2)


def stopMoving(g: Game):
    if g.santa.vx != 0:
        if g.santa.vx > 0:
            g.accelerate(g.santa.vx, ACCELERATE_LEFT)
        else:
            g.accelerate(-g.santa.vx, ACCELERATE_RIGHT)
        if g.timeCount + 1 < g.timeLimit:
            g.floatX(1)
        else:
            finish(g)

    if g.santa.vy != 0:
        if g.santa.vy > 0:
            g.accelerate(g.santa.vy, ACCELERATE_DOWN)
        else:
            g.accelerate(-g.santa.vy, ACCELERATE_UP)
        if g.timeCount + 1 < g.timeLimit:
            g.floatX(1)
        else:
            finish(g)


def getMap(g: Game):
    x = [gift.x for gift in g.toDeliver]
    y = [gift.y for gift in g.toDeliver]

    return min(x), max(x), min(y), max(y)


def getGiftsInArea(x, y, g: Game):
    gifts = []
    amount = 0
    for gift in g.toDeliver:
        if getDist(x, y, gift.x, gift.y) <= g.maxDeliveryDistance:
            gifts.append(gift)
            amount += 1

    return gifts


def goTo(x: int, y: int, g: Game, goFast: bool = True):

    distX = abs(g.santa.x - x)
    distY = abs(g.santa.y - y)

    if g.santa.getMaxAcc() is not None or g.santa.carrots <= 0:
        return

    if goFast:
        x1 = int(abs(g.santa.x - x) / 2)
        if g.santa.x < x:
            while g.santa.x < x1:
                if g.santa.x + g.santa.vx + g.santa.getMaxAcc() > x1:
                    break

                if g.timeCount + 1 >= g.timeLimit or g.santa.carrots <= 0:
                    finish(g)

                g.accelerate(g.santa.getMaxAcc(), ACCELERATE_RIGHT)
                g.floatX(1)

            while g.santa.vx > 0:
                if g.timeCount + 1 >= g.timeLimit or g.santa.carrots <= 0:
                    finish(g)

                g.accelerate(g.santa.getMaxAcc(), ACCELERATE_LEFT)
                g.floatX(1)

        elif g.santa.x > x:
            while g.santa.x > x1:
                if g.santa.x + g.santa.vx - g.santa.getMaxAcc() < x1:
                    break
                if g.timeCount + 1 >= g.timeLimit or g.santa.carrots <= 0:
                    finish(g)
                g.accelerate(g.santa.getMaxAcc(), ACCELERATE_LEFT)
                g.floatX(1)
            while g.santa.vx < 0:
                if g.timeCount + 1 >= g.timeLimit or g.santa.carrots <= 0:
                    finish(g)
                g.accelerate(g.santa.getMaxAcc(), ACCELERATE_RIGHT)
                g.floatX(1)

    if distY > g.santa.getMaxAcc():
        y1 = int(abs(g.santa.y - y) / 2)
        if g.santa.y < y:
            while g.santa.y < y1:
                if g.santa.y + g.santa.vy + g.santa.getMaxAcc() > y1:
                    break
                if g.timeCount + 1 >= g.timeLimit or g.santa.carrots <= 0:
                    finish(g)
                g.accelerate(g.santa.getMaxAcc(), ACCELERATE_UP)
                g.floatX(1)

            while g.santa.vy > 0:
                if g.timeCount + 1 >= g.timeLimit or g.santa.carrots <= 0:
                    finish(g)
                g.accelerate(g.santa.getMaxAcc(), ACCELERATE_DOWN)
                g.floatX(1)

        elif g.santa.y > y:
            while g.santa.y > y1:
                if g.santa.y + g.santa.vy - g.santa.getMaxAcc() < y1:
                    break
                if g.timeCount + 1 >= g.timeLimit or g.santa.carrots <= 0:
                    finish(g)
                g.accelerate(g.santa.getMaxAcc(), ACCELERATE_DOWN)
                g.floatX(1)
            while g.santa.vy < 0:
                if g.timeCount + 1 >= g.timeLimit or g.santa.carrots <= 0:
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
                    g.accelerate(abs(max_acc - distX), ACCELERATE_LEFT)
                elif g.santa.vx == 0:
                    g.accelerate(distX if distX < max_acc else max_acc, ACCELERATE_RIGHT)

                if g.timeCount + 1 < g.timeLimit or g.santa.carrots <= 0:
                    g.floatX(1)
                else:
                    finish(g)

                if g.santa.x >= x:
                    stopMoving(g)

            else:
                g.accelerate(max_acc, ACCELERATE_RIGHT)
                tf = distX // max_acc

                if g.timeCount + tf < g.timeLimit or g.santa.carrots <= 0:
                    g.floatX(tf)
                else:
                    g.floatX(g.timeLimit - g.timeCount)
                    finish(g)

                if g.santa.x >= x:
                    stopMoving(g)
        else:
            max_acc = g.santa.getMaxAcc()
            if distX < max_acc:
                if g.santa.vx < 0:
                    g.accelerate(abs(max_acc - distX), ACCELERATE_RIGHT)
                elif g.santa.vx == 0:
                    g.accelerate(distX if distX < max_acc else max_acc, ACCELERATE_LEFT)

                if g.timeCount + 1 < g.timeLimit or g.santa.carrots <= 0:
                    g.floatX(1)
                else:
                    finish(g)
                if g.santa.y >= y:
                    stopMoving(g)
            else:
                g.accelerate(max_acc, ACCELERATE_LEFT)
                tf = distX // max_acc

                if g.timeCount + tf < g.timeLimit or g.santa.carrots <= 0:
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
                    g.accelerate(abs(max_acc - distY), ACCELERATE_DOWN)
                elif g.santa.vy == 0:
                    g.accelerate(distY if distY < max_acc else max_acc, ACCELERATE_UP)
                if g.timeCount + 1 < g.timeLimit or g.santa.carrots <= 0:
                    g.floatX(1)
                else:
                    finish(g)
                stopMoving(g)
            else:
                g.accelerate(max_acc, ACCELERATE_UP)
                tf = distY // max_acc

                if g.timeCount + tf < g.timeLimit or g.santa.carrots <= 0:
                    g.floatX(tf)
                else:
                    if g.timeLimit - g.timeCount <= g.timeLimit or g.santa.carrots <= 0:
                        g.floatX(g.timeLimit - g.timeCount)
                    finish(g)

                if g.santa.y > y:
                    stopMoving(g)
        else:
            max_acc = g.santa.getMaxAcc()
            if distY < max_acc:
                if g.santa.vy < 0:
                    g.accelerate(abs(max_acc - distY), ACCELERATE_UP)
                elif g.santa.vy == 0:
                    g.accelerate(distY if distY < max_acc else max_acc, ACCELERATE_DOWN)
                if g.timeCount + 1 < g.timeLimit or g.santa.carrots <= 0:
                    g.floatX(1)
                else:
                    finish(g)
                stopMoving(g)
            else:
                g.accelerate(max_acc, ACCELERATE_DOWN)
                tf = distY // max_acc

                if g.timeCount + tf < g.timeLimit or g.santa.carrots <= 0:
                    g.floatX(tf)
                else:
                    if g.timeLimit - g.timeCount <= g.timeLimit or g.santa.carrots <= 0:
                        g.floatX(g.timeLimit - g.timeCount)
                    finish(g)

                if g.santa.y < y:
                    stopMoving(g)

    print(f"{g.timeCount}/{g.timeLimit} done y {g.santa.vx} {g.santa.x, g.santa.y}")
    stopMoving(g)


def clusters_analysis(g: Game):
    minX, maxX, minY, maxY = getMap(g)
    ga = []
    score = 0
    for gift in g.toDeliver:
        if gift.x >= minX and gift.x <= maxX and gift.y >= minY and gift.y <= maxY:
            ga.append(gift)
            score += gift.score
    print(len(ga), score)

    # Algorithm DBSCAN
    visited_points = []
    clusters = []
    for point in ga:
        if point in visited_points:
            continue
        visited_points.append(point)
        cluster = [point]
        for point2 in ga:
            if point2 in visited_points:
                continue
            if getDist(point.x, point.y, point2.x, point2.y) <= 300:
                cluster.append(point2)
                visited_points.append(point2)
        clusters.append(cluster)

    # sort the clusters by making the average x and y of the cluster and sort by the distance to 0,0
    return sorted(clusters, key=lambda x: getDist(0, 0, sum([i.x for i in x]) / len(x), sum([i.y for i in x]) / len(x)))


def cluster_delivery(clusters, g: Game):
    for i in clusters:
        print(f"Cluster {clusters.index(i)}: len: {len(i)}, weight: {sum([j.weight for j in i])}, score: {sum([j.score for j in i])}")

    for i in range(len(clusters)):
        index = 0
        while index < len(clusters[i]):
            if g.santa.getDistance(0, 0) <= g.maxDeliveryDistance:
                if g.santa.carrots > 0:
                    goTo(0, 0, g, False)
                    g.loadCarrots(101 - g.santa.carrots)
                else:
                    goTo(0, 0, g)
                    g.loadCarrots(101)

            for gift in clusters[i]:
                if gift in g.toDeliver and gift not in g.deliveredGifts and g.santa.weight + gift.weight < g.santa.getMaxWeight() and g.santa.getDistance(0, 0) <= g.maxDeliveryDistance:
                    print(gift)
                    g.loadGift(gift)
                    index += 1

            g.santa.loadedGifts = sorted(g.santa.loadedGifts, key=lambda x: getDist(0, 0, x.x, x.y))

            for gift in g.santa.loadedGifts:
                goTo(gift.x, gift.y, g, False)
                if g.santa.getDistance(gift.x, gift.y) <= g.maxDeliveryDistance:
                    g.deliverGift(gift)
                    print(f"Deliver {gift}")
            goTo(0, 0, g, False)


def generate_coordinates(g):
    minX, maxX, minY, maxY = getMap(g)
    coordinates = []
    for i in range(minX, maxX, g.maxDeliveryDistance if g.maxDeliveryDistance else 1):
        for j in range(minY, maxY, g.maxDeliveryDistance if g.maxDeliveryDistance else 1):
            coordinates.append((i, j))

    return coordinates


def area_analysis(g):
    coordinates = generate_coordinates(g)
    temp = []
    for i in coordinates:
        score = 0
        for gift in g.toDeliver:
            if getDist(gift.x, gift.y, i[0], i[1]) <= g.maxDeliveryDistance:
                score += gift.score
        if score > 0:
            temp.append((i[0], i[1], score))
    temp = list(set(temp))
    temp.sort(key=lambda x: x[2] / (getDist(x[0], x[1], 0, 0) + 1), reverse=True)

    return temp


def area_delivery(coordinates, g):
    for i in range(len(coordinates)):
        g.toDeliver.sort(key=lambda x: getDist(x.x, x.y, coordinates[i][0], coordinates[i][1]))
        goTo(0, 0, g)
        print(f"{g.santa.x} {g.santa.y}")
        g.loadCarrots(100)
        if g.santa.getDistance(0, 0) <= g.maxDeliveryDistance:
            for j in range(len(g.toDeliver)):
                if getDist(g.toDeliver[0].x, g.toDeliver[0].y, coordinates[i][0], coordinates[i][1]) <= g.maxDeliveryDistance:
                    g.loadGift(g.toDeliver[0])

        goTo(coordinates[i][0], coordinates[i][1], g)
        print(f"{g.santa.x} {g.santa.y} ")
        for i in range(len(g.santa.loadedGifts)):
            print(f"{g.santa.loadedGifts[0]}")
            if g.santa.getDistance(g.santa.loadedGifts[0].x, g.santa.loadedGifts[0].y) <= g.maxDeliveryDistance:
                g.deliverGift(g.santa.loadedGifts[0])
            else:
                g.santa.loadedGifts.remove(g.santa.loadedGifts[0])
