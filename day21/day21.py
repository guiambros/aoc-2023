import operator
import os
import re
import sys
import time
from collections import defaultdict
from copy import deepcopy
from functools import cache, lru_cache, reduce

import networkx as nx


def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} took {end_time - start_time} seconds to run.")
        return result

    return wrapper


# get current day from path and read input data
cwd = sys.argv[0]
if not ("day" in cwd):
    print("Run this from the day directory")
    sys.exit(0)
year = int(re.search("\\d{4}", cwd).group(0))
day = int(re.search("\\/day(\\d+)", cwd).group(1))
input = open(f"day{day}/input_{year}_{day}.txt", "r").read()


GPS = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "W": (0, -1)}


def print_map(M, visited):
    for r, row in enumerate(M):
        for c, char in enumerate(row):
            if (r, c) in visited:
                print("O", end="")
            else:
                print(char, end="")
        print()


@timer
def part1(G, start, max_steps=64):
    steps = 0
    nodes = {start}
    while steps < max_steps:
        nodes = set(
            [
                G.nodes[n][d]
                for n in nodes
                for d in [key for key in G.nodes[n].keys() if key != "ch"]
            ]
        )
        steps += 1
    print(f"Part 1: unique plots visited {len(nodes)}")
    return len(nodes)


def part2(G, start, max_steps=1000):
    steps = part1(G, start, max_steps=max_steps)
    print(f"Part 2: {steps}")
    return steps


if __name__ == "__main__":
    # reads input data and creates a graph
    G = nx.Graph()
    G2 = nx.Graph()

    M = [line for line in input.splitlines()]
    h = len(M)
    w = len(M[0])
    row = [r for r, line in enumerate(M) if "S" in line][0]
    col = [c for c, char in enumerate(M[row]) if char == "S"][0]
    start = (row, col)
    for r, row in enumerate(M):
        for c, char in enumerate(row):
            G.add_node((r, c), ch=char)
            G2.add_node((r, c), ch=char)

            if char != "#":
                for direction in GPS:
                    pos = tuple(map(operator.add, (r, c), GPS[direction]))

                    # Part 1
                    if 0 <= pos[0] < h and 0 <= pos[1] < w and M[pos[0]][pos[1]] != "#":
                        G.nodes[(r, c)][direction] = pos
                        G2.nodes[(r, c)][direction] = pos

                    # Part 2: add wrapping around edges
                    if pos[0] in [-1, h + 1] or pos[1] in [-1, w + 1]:
                        # and
                        pos = ((pos[0] + h) % h, (pos[1] + w) % w)
                        if M[(pos[0] + h) % h][(pos[1] + w) % w] != "#":
                            assert pos[0] >= 0
                            assert pos[1] >= 0
                            G2.nodes[(r, c)][direction] = pos

    part1(G, start, max_steps=64)  ## 3841

    # Part 2 is not going to work; need to look at the data and do it geometrically. Hate this
    # type of puzzles. Going to skip it.
    #
    # This is a good explanation of the solution:
    # https://github.com/villuna/aoc23/wiki/A-Geometric-solution-to-advent-of-code-2023,-day-21
    #
    # And here's a few solutions:
    # https://github.com/democat3457/AdventOfCode/blob/ee5e3d922dde8330d49fc038942d61ff47254965/2023/day21.py
    # https://github.com/Fadi88/AoC/blob/master/2023/day21/code.py
    #
    #
    # part2(G2, start, max_steps=400)  ## 636391426712747
