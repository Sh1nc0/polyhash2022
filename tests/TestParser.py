import sys
sys.path.insert(1, '../src')
from parser import Parser

data_path = "../data/input_data"


def testFileA():
    p = Parser(f"{data_path}/a_an_example.in.txt")
    p.parse()

    assert p.time == 15
    assert p.deliveryDistance == 3
    assert p.nbAcc == 4
    assert p.nbGifts == 4
    assert p.santa.maxSpeed == [(15, 8), (30, 6), (45, 4), (60, 2)]
    assert p.nbGifts == len(p.gifts)


def testFileB():
    p = Parser(f"{data_path}/b_better_hurry.in.txt")
    p.parse()

    assert p.time == 450
    assert p.deliveryDistance == 100
    assert p.nbAcc == 5
    assert p.nbGifts == 1000
    assert p.santa.maxSpeed == [(2000, 20), (3000, 15), (5000, 10), (6000, 9), (7000, 8)]
    assert p.nbGifts == len(p.gifts)


def testFileC():
    p = Parser(f"{data_path}/c_carousel.in.txt")
    p.parse()

    assert p.time == 5000
    assert p.deliveryDistance == 10
    assert p.nbAcc == 3
    assert p.nbGifts == 10000
    assert p.santa.maxSpeed == [(10000, 4), (20000, 2), (40000, 1)]
    assert p.nbGifts == len(p.gifts)


def testFileD():
    p = Parser(f"{data_path}/d_decorated_houses.in.txt")
    p.parse()

    assert p.time == 10000
    assert p.deliveryDistance == 0
    assert p.nbAcc == 1
    assert p.nbGifts == 5000
    assert p.santa.maxSpeed == [(1000, 100)]
    assert p.nbGifts == len(p.gifts)


def testFileE():
    p = Parser(f"{data_path}/e_excellent_weather.in.txt")
    p.parse()

    assert p.time == 1200
    assert p.deliveryDistance == 30
    assert p.nbAcc == 7
    assert p.nbGifts == 10000
    assert p.santa.maxSpeed == [(16000, 10), (20000, 9), (24000, 7), (28000, 5), (32000, 3), (36000, 2), (40000, 1)]
    assert p.nbGifts == len(p.gifts)


def testFileF():
    p = Parser(f"{data_path}/f_festive_flyover.in.txt")
    p.parse()

    assert p.time == 600
    assert p.deliveryDistance == 20
    assert p.nbAcc == 3
    assert p.nbGifts == 10000
    assert p.santa.maxSpeed == [(10000, 4), (20000, 2), (40000, 1)]
    assert p.nbGifts == len(p.gifts)


def test():
    testFileA()
    testFileB()
    testFileC()
    testFileD()
    testFileE()
    testFileF()


if __name__ == "__main__":
    test()
    print("All tests passed")