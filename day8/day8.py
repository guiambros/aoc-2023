import itertools
import math
import re
import sys
from functools import reduce
from math import lcm

# get current day
cwd = sys.argv[0]
if not ("day" in cwd):
    print("Run this from the day directory")
    sys.exit(0)

# read input data
year = int(re.search("\\d{4}", cwd).group(0))
day = int(re.search("\\/day(\\d+)", cwd).group(1))

input = open(f"day{day}/input_{year}_{day}.txt", "r").read()
input = [line for line in input.splitlines()]


def part1(M, path):
    cnt = 0
    current_node = "AAA"
    path_iter = itertools.cycle(path)
    while current_node != "ZZZ":
        pathLR = next(path_iter)
        # print(f"Visiting { current_node } taking path {'R' if pathLR == 1 else 'L' }")
        current_node = M[current_node][pathLR]
        cnt += 1
    print(f"Part 1: {cnt}")
    pass


def part2(M, path):
    nodes = [n for n in M.keys() if n[2] == "A"]
    num_cursors = len(nodes)

    # brute force doesn't work; some cycles are likely way too long
    # cnt = 0
    # while not all([n[2] == "Z" for n in cur_nodes]):
    #     pathLR = next(path)
    #     cur_nodes = [M[cur_nodes[i]][pathLR] for i in range(num_cursors)]
    #     cnt += 1

    cycles = []
    for i, node in enumerate(nodes):
        cycle_len = 0
        path_iter = itertools.cycle(path)

        while node[-1] != "Z":  # search for cycle
            node = M[node][next(path_iter)]
            cycle_len += 1
        print(f"Found cycle for {nodes[i]} at {cycle_len} times")
        cycles.append(cycle_len)
    print(f"Part 2: lcm of {cycles} == {math.lcm(*cycles)}")


if __name__ == "__main__":
    M = dict()
    # parse the first line
    path = [int(c.replace("L", "0").replace("R", "1")) for c in input[0]]
    SIZE = len(path)

    # parse the remaining lines
    i = 2
    while i < len(input):
        l = input[i].replace("= (", "").replace(",", "").replace(")", "").split(" ")
        dst, pathL, pathR = l[0], l[1], l[2]
        M[dst] = (pathL, pathR)
        i += 1

    part1(M, path)
    part2(M, path)
