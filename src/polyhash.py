from objects.game import Game
from parser import Parser
import argparse

from util.functions import clusters_analysis, cluster_delivery, area_analysis, area_delivery, finish

if __name__ == "__main__":
    """
    Main function
        this function is the entry point of the program it parses the input file and creates the game object then it calls the different alogrithm to solve the challenge

    Run the program with the following command in the src folder:
        python3 polyhash.py "challenge.txt"

        you will find the input files in ../data/input_data/
        you will find the output files in ../data/output_data/
    """

    args = argparse.ArgumentParser(description='File Input')
    args.add_argument('fileInput', type=str, help='challenge definition filename', metavar="challenge.txt")
    args = args.parse_args()

    p = Parser(args.fileInput)
    p.parse()

    g = Game(p)
    clusters = clusters_analysis(g)

    if len(clusters) >= 25:
        cluster_delivery(clusters, g)

    else:
        print("Analyse des différente zones")
        coordinates = area_analysis(g)

        print("Livraison des cadeaux")
        area_delivery(coordinates, g)
    finish(g)
    print(f"score : {g.score}")