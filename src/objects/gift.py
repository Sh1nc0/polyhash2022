#!/usr/bin/env python3
# -*- coding: utf-8 -*-
class Gift:
    """
    Gift object
        This object represents a gift
    Attributes
    ----------
    name : str
        Name of the gift

    score : int
        Score of the gift

    weight : int
        Weight of the gift

    x : int
        X coordinate of the gift

    y : int
        Y coordinate of the gift
    """

    def __init__(self, name: str, score: int, weight: int, x: int, y: int):
        """
        Parameters
        ----------
        name : str
            Name of the gift

        score : int
            Score of the gift

        weight : int
            Weight of the gift

        x : int
            X coordinate of the gift

        y : int
            Y coordinate of the gift
        """
        self.name: str = name
        self.score: int = score
        self.weight: int = weight
        self.x: int = x
        self.y: int = y

    def __str__(self) -> str:
        """
        Returns
        -------
        str
            String representation of the gift
        """
        return f"Gift: {self.name} {self.score} {self.weight} {self.x} {self.y}"
