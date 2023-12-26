import operator
import os
import re
import sys
import time
from collections import defaultdict
from copy import deepcopy
from functools import cache, lru_cache, reduce


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


def part1(input):
    print(f"Part 1: {None}")
    pass


def part2(input):
    print(f"Part 2: {None}")
    pass


import matplotlib.pyplot as plt


def print_graph(G):
    pos = nx.spring_layout(G)  # positions for all nodes

    # nodes
    nx.draw_networkx_nodes(G, pos)

    # edges
    nx.draw_networkx_edges(G, pos)

    # labels
    nx.draw_networkx_labels(G, pos, font_size=10, font_color="white")

    plt.show()


import networkx as nx

if __name__ == "__main__":
    G = nx.Graph()

    for line in input.splitlines():
        node, nodes = line.split(": ")
        nodes = nodes.split(" ")
        G.add_node(node)
        for n in nodes:
            G.add_node(n)
            G.add_edge(node, n)

    # cut the wires
    G.remove_edge("btp", "qxr")
    G.remove_edge("bqq", "rxt")
    G.remove_edge("vfx", "bgl")

    components = nx.connected_components(G)
    for i, component in enumerate(components, start=1):
        print(f"Group {i} has {len(component)} nodes")
    print_graph(G)


# 1,593,412,464
