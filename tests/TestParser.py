import sys
sys.path.insert(1, '../src')
from parser import Parser

data_path = "../data/input_data"


def testFileA():
    p = Parser(f"{data_path}/a_an_example.in.txt")
    p.parse()

def test():
    testFileA()