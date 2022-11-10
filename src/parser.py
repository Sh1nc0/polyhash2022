#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from objects.deliveryPoint import DeliveryPoint

"""Module de parsing des fichiers d'entrée pour la mise en oeuvre du projet Poly#.
"""


def parse_challenge(filename: str) -> object:
    """Lit un fichier de challenge et extrait les informations nécessaires.
    """

    with open(filename, "r") as f:
        lines = f.readlines()

    config = {}
    deliveryPoints = []
    accRange = {}

    for line in lines:
        properties = line.split(" ")
        if len(properties) == 4:  # config
            config["time"] = int(properties[0])
            config["deliveryDistance"] = int(properties[1])
            config["nbAccRange"] = int(properties[2])
            config["nbGifts"] = int(properties[3])

        if len(properties) == 2:  # accRange
            accRange[int(properties[0])] = int(properties[1])

        if len(properties) == 5:  # DeliveryPoint
            deliveryPoints.append(DeliveryPoint(
                properties[0], properties[1], properties[2], properties[3], properties[4]))

    return config, deliveryPoints, accRange
