#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from parser import parse_challenge
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Solve Poly# challenge.')
    parser.add_argument('challenge', type=str,
                        help='challenge definition filename', metavar="challenge.txt")
    args = parser.parse_args()
    challenge = parse_challenge(args.challenge)

    # TODO: Parse the challenge
    # TODO: Solve the challenge
