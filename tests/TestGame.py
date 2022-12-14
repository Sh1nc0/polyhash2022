import sys
sys.path.insert(1, '../src')
from parser import Parser
from objects.gift import Gift
from objects.game import Game
from util.constants import *

data_path = "../data/input_data"

def testFileA():
    p = Parser(f"{data_path}/a_an_example.in.txt")
    p.parse()

    g = Game(p)

    assert g.timeLimit == 15
    assert g.maxDeliveryDistance == 3
    assert len(g.santa.maxSpeed) == 4
    assert len(g.toDeliver) == 4
    assert g.santa.maxSpeed == [(15,8),(30,6),(45,4),(60,2)]

def testFileB():
    p = Parser(f"{data_path}/b_better_hurry.in.txt")
    p.parse()

    g = Game(p)

    assert g.timeLimit == 450
    assert g.maxDeliveryDistance == 100
    assert len(g.santa.maxSpeed) == 5
    assert len(g.toDeliver) == 1000
    assert g.santa.maxSpeed == [(2000,20),(3000,15),(5000,10),(6000,9),(7000,8)]

def testFunctions():
    p = Parser(f"{data_path}/a_an_example.in.txt")
    p.parse()

    g = Game(p)

    g.loadCarrots(10)
    assert g.santa.carrots == 10

    g.loadGift(g.toDeliver[0])
    assert len(g.santa.loadedGifts) > 0
    assert g.santa.loadedGifts[0].name == "Olivia" and g.santa.loadedGifts[0].score == 1 and g.santa.loadedGifts[0].weight == 10 and g.santa.loadedGifts[0].x == 5 and g.santa.loadedGifts[0].y == 1
    assert g.santa.weight == 20

    g.accelerate(1, ACCELERATE_UP)
    assert g.santa.vy == 1
    assert g.santa.carrots == 9

    g.accelerate(5, ACCELERATE_RIGHT)
    assert g.santa.vx == 5
    assert g.santa.carrots == 8

    g.floatX(1)
    assert g.timeCount == 1
    assert g.santa.x == 5 and g.santa.y == 1

    g.deliverGift(g.santa.loadedGifts[0])
    assert len(g.santa.loadedGifts) == 0  

    assert len(g.outputString) == 6


def test():
    testFileA()
    testFileB()
    testFunctions()


if __name__ == "__main__":
    test()
    print("All tests passed")