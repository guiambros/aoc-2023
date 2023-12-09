import operator
import os
import re
import sys
from collections import defaultdict
from copy import deepcopy
from functools import reduce

# get current day
cwd = sys.argv[0]
if not ("day" in cwd):
    print("Run this from the day directory")
    sys.exit(0)

# read input data
# year = int(re.search("\\d{4}", cwd).group(0))
# day = int(re.search("\\/day(\\d+)", cwd).group(1))
year = "2023"
day = "8"

input = open(f"day{day}/input_{year}_{day}.txt", "r").read()
# input = open(f"day{day}/input_{year}_{day}_test.txt", "r").read()

# input in multiple lines
input = [line for line in input.splitlines()]

import itertools


def part1(M, directions_queue):
    dst = "ZZZ"
    cnt = 0
    path = itertools.cycle(directions_queue)
    current_node = "AAA"
    while current_node != dst:
        pathLR = next(path)
        print("Visiting", current_node, "taking path ", "R" if pathLR == 1 else "L")
        current_node = M[current_node][pathLR]
        cnt += 1
    print(f"Part 1: {cnt}")
    pass


def part2(M, directions_queue):
    cur_nodes = [n for n in M.keys() if n[2] == "A"]
    num_cursors = len(cur_nodes)
    path = itertools.cycle(directions_queue)

    # brute force doesn't work; some cycles are likely way too long
    # cnt = 0
    # while not all([n[2] == "Z" for n in cur_nodes]):
    #     pathLR = next(path)
    #     cur_nodes = [M[cur_nodes[i]][pathLR] for i in range(num_cursors)]
    #     cnt += 1

    lcm = []
    for i in range(num_cursors):
        found, visited2 = False, []
        node = cur_nodes[i]
        ptr = 0
        while found == False:
            idx = ptr % len(directions_queue)
            if ((node, idx)) in visited2:
                print(f"Found cycle for {cur_nodes[i]} at {ptr} times")
                lcm.append(ptr)
                found = True
                break
            visited2.append((node, idx))
            ptr += 1
            pathLR = next(path)
            node = M[node][pathLR]
        break

    print(f"Part 2: lcm of {lcm}")
    pass

    path = itertools.cycle(directions_queue)
    lcm = []
    size = len(directions_queue)
    for node in cur_nodes:
        visited2 = []
        idx = 0
        cycle_len = 0
        cur_node = node
        while ((cur_node, idx)) not in visited2:
            idx = cycle_len % len(directions_queue)
            visited2.append((cur_node, idx))
            cycle_len += 1
            pathLR = next(path)
            print(f"Visiting {cur_node}, taking path { 'R' if pathLR == 1 else 'L'}")
            cur_node = M[cur_node][pathLR]
        print(f"Found cycle for cursor {node} at {cycle_len} times")
        lcm.append(cycle_len)
    # lcm_d = reduce(lambda x, y: x * y // math.gcd(x, y), lcm)
    print(f"Part 2: lcm of {lcm} == {lcm_d}")
    pass


if __name__ == "__main__":
    directions_queue = [int(c.replace("L", "0").replace("R", "1")) for c in input[0]]
    i = 2
    M = dict()
    while i < len(input):
        l = input[i].replace("= (", "").replace(",", "").replace(")", "").split(" ")
        dst, pathL, pathR = l[0], l[1], l[2]
        M[dst] = (pathL, pathR)
        i += 1
    print(M)
    # part1(M, directions_queue)
    part2(M, directions_queue)
