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


def longest_simple_path(G, start, finish):
    longest_path = []
    for path in nx.all_simple_paths(G, source=start, target=finish):
        if len(path) > len(longest_path):
            longest_path = path
    return longest_path


def part1(G):
    path = longest_simple_path(G, start, finish)
    print(f"Part 1: {len(path)-1}")
    print_map(G, path)
    pass


def part2(input):
    print(f"Part 2: {None}")
    pass


def print_map(M, visited):
    for r, row in enumerate(input):
        for c, char in enumerate(row):
            if (r, c) in visited and input[r][c] == ".":
                print("O", end="")
            elif input[r][c] == "#":
                print(" ", end="")
            else:
                print(char, end="")
        print()


def plot_graph(G):
    pass
    # import matplotlib.pyplot as plt

    # plt.figure(figsize=(8, 6))  # Set the size of the figure
    # nx.draw_networkx(G, with_labels=False, node_size=10)  # Draw the graph
    # plt.savefig("graph.png")  # Save the figure as a PNG image
    # plt.show()  # Display the figure


if __name__ == "__main__":
    input = [line for line in input.splitlines()]

    GPS = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}
    h = len(input)
    w = len(input[0])
    start = (0, 1)
    finish = (140, 139)
    # finish = (22, 21)
    G = nx.DiGraph()

    for r in range(len(input)):
        for c in range(len(input[r])):
            if input[r][c] in [".", "<", ">", "^", "v"]:
                G.add_node((r, c), slope=input[r][c])

    # connect edges
    for node in G.nodes:
        r, c = node

        if input[r][c] != ".":  # we're on a slope; connect only to the directio it points to
            G.add_edge(node, (r + GPS[input[r][c]][0], c + GPS[input[r][c]][1]))
            continue

        for direction, (dr, dc) in GPS.items():
            ch = "#" if r + dr >= h or c + dc >= w else input[r + dr][c + dc]
            if ch == "#":
                continue

            if (r + dr, c + dc) in G.nodes and input[r + dr][c + dc] != "#":
                ch = input[r + dr][c + dc]
                if ch == "." or ch == direction:
                    G.add_edge(node, (r + dr, c + dc))

    part1(G)
    part2(G)
