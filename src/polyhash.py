from objects.game import Game
from parser import Parser
import argparse

from util.functions import clusters_analysis, cluster_delivery, area_analysis, area_delivery, finish

if __name__ == "__main__":

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
    g.finish()
    print(f"score : {g.score}")