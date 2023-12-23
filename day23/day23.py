import logging
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
    import matplotlib.pyplot as plt

    plt.figure(figsize=(8, 6))  # Set the size of the figure
    nx.draw_networkx(G, with_labels=False, node_size=10)  # Draw the graph
    plt.savefig("graph.png")  # Save the figure as a PNG image
    plt.show()  # Display the figure
    pass


def connect_edges(G, is_part2=False):
    for node in G.nodes:
        r, c = node

        if input[r][c] != "." and not is_part2:
            # we're on a slope; connect only to the direction it points to
            G.add_edge(node, (r + GPS[input[r][c]][0], c + GPS[input[r][c]][1]))
            continue

        for direction, (dr, dc) in GPS.items():
            ch = "#" if r + dr >= h or c + dc >= w else input[r + dr][c + dc]
            if ch == "#":
                continue

            if (r + dr, c + dc) in G.nodes and input[r + dr][c + dc] != "#":
                ch = input[r + dr][c + dc]
                if ch == "." or (ch == direction or is_part2):
                    G.add_edge(node, (r + dr, c + dc))

    return G


def manhattan_distance(a, b):
    return 1 / (abs(a[0] - b[0]) + abs(a[1] - b[1]) + 1e-10)


def longest_path_astar(G, start, finish):
    # Add a weight of 1 to all edges
    for u, v, data in G.edges(data=True):
        data["weight"] = 10

    # Use the A* algorithm to find the shortest path
    path = nx.astar_path(
        G, source=start, target=finish, heuristic=manhattan_distance, weight="weight"
    )

    return path


def longest_path_dijkstra(G, start, finish):
    # Add a weight of 1 to all edges
    for u, v, data in G.edges(data=True):
        data["weight"] = 10

    # Use Dijkstra's algorithm to find the shortest path
    path = nx.longest_path_astar(G, source=start, target=finish, weight="weight")

    return path


from collections import deque


def longest_path_dfs(G, start, finish):
    stack = deque([(start, [start])])
    longest_path = []
    while stack:
        (node, path) = stack.pop()
        for next in set(G[node]) - set(path):
            if next == finish:
                longest_path = max(longest_path, path + [next], key=len)
            else:
                stack.append((next, path + [next]))
    return longest_path


def inverse_manhattan_distance(a, b):
    return 1 / (abs(a[0] - b[0]) + abs(a[1] - b[1]) + 1e-10)


def longest_path_dfs_v2(G, start, finish):
    stack = deque([(start, [start])])
    longest_path = []
    while stack:
        (node, path) = stack.pop()
        neighbors = list(set(G[node]) - set(path))
        # Sort the neighbors by their inverse Manhattan distance to the finish node
        neighbors.sort(key=lambda x: inverse_manhattan_distance(x, finish), reverse=True)
        for next in neighbors:
            if next == finish:
                longest_path = max(longest_path, path + [next], key=len)
                logging.info(f"Longest path so far: {len(longest_path) - 1}")
            else:
                stack.append((next, path + [next]))
    return longest_path


def longest_simple_path(G, start, finish, cutoff):
    longest_path = []
    for path in nx.all_simple_paths(G, source=start, target=finish, cutoff=cutoff):
        if len(path) > len(longest_path):
            longest_path = path
    return longest_path


@timer
def part1(G):
    connect_edges(G)
    path = longest_simple_path(G, start, finish, cutoff=10000)
    print(f"Part 1: {len(path)-1}")
    print_map(G, path)


@timer
def part2(input):
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    connect_edges(G, is_part2=True)
    # path = longest_simple_path(G, start, finish, cutoff=10000)  # too slow for part2
    # path = nx.dag_longest_path(G, start, finish) # only works on DAGs (no cycles)
    # path = longest_path_astar(G, start, finish)  # too short (1382); even shorted than pt1
    path = longest_path_dfs_v2(G, start, finish)
    print(f"Part 1: {len(path)-1}")
    print_map(G, path)


if __name__ == "__main__":
    input = [line for line in input.splitlines()]

    GPS = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}
    h = len(input)
    w = len(input[0])
    start = (0, 1)
    finish = (h - 1, w - 2)
    G = nx.DiGraph()

    for r in range(len(input)):
        for c in range(len(input[r])):
            if input[r][c] in [".", "<", ">", "^", "v"]:
                G.add_node((r, c), slope=input[r][c])

    # part1(G.copy()) # 2190
    part2(G.copy())  # 6258
