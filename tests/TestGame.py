import sys
sys.path.insert(1, '../src')
from parser import Parser
from objects.gift import Gift
from objects.game import Game

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

def test():
    testFileA()
    testFileB()

if __name__ == "__main__":
    test()
    print("All tests passed")