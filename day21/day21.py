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
def part1_bruteforce(max_steps=64):
    # brute force the solution. Works for small maps and few steps (<15), but
    # exponential growth makes it infeasible for larger maps
    #
    visited = defaultdict(list)
    to_visit = []

    def visit_plot(pos, steps):
        to_visit.append((pos, steps))

        while steps <= max_steps:
            pos, steps = to_visit.pop(0)
            visited[steps].append(pos)
            # print_map(M, visited)

            all_pos = [tuple(map(operator.add, pos, GPS[direction])) for direction in GPS]
            valid_pos = [
                pos
                for pos in all_pos
                if 0 <= pos[0] < h and 0 <= pos[1] < w and M[pos[0]][pos[1]] != "#"
            ]
            for pos in valid_pos:
                to_visit.append((pos, steps + 1))
        return

    visit_plot(start, 0)
    print(f"Part 1: unique plots visited {len(set(visited[max_steps]))}")
    pass


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
    pass


def part2():
    print(f"Part 2: {None}")
    pass


if __name__ == "__main__":
    # reads input data and creates a graph
    G = nx.Graph()
    M = [line for line in input.splitlines()]
    h = len(M)
    w = len(M[0])
    row = [r for r, line in enumerate(M) if "S" in line][0]
    col = [c for c, char in enumerate(M[row]) if char == "S"][0]
    start = (row, col)
    for r, row in enumerate(M):
        for c, char in enumerate(row):
            G.add_node((r, c), ch=char)
            if char != "#":
                for direction in GPS:
                    pos = tuple(map(operator.add, (r, c), GPS[direction]))
                    if 0 <= pos[0] < h and 0 <= pos[1] < w and M[pos[0]][pos[1]] != "#":
                        G.nodes[(r, c)][direction] = pos

    # part1_bruteforce(max_steps=13)
    part1(G, start, max_steps=64)
    part2()
