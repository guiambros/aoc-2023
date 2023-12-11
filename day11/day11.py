import operator
import os
import re
import sys
from collections import defaultdict
from copy import deepcopy
from functools import reduce
from itertools import combinations

# get current day
cwd = sys.argv[0]
if not ("day" in cwd):
    print("Run this from the day directory")
    sys.exit(0)

# read input data
year = int(re.search("\\d{4}", cwd).group(0))
day = int(re.search("\\/day(\\d+)", cwd).group(1))


input = open(f"day{day}/input_{year}_{day}.txt", "r").read()
# input = open(f"day{day}/input_{year}_{day}_test.txt", "r").read()
input = [line for line in input.splitlines()]
input = [[ch for ch in input[x]] for x in range(len(input))]
h = len(input)
w = len(input[0])

rows_to_add, cols_to_add = [], []


def expand_map(M, is_part2=False):
    galaxies = []
    rows_to_add.clear()
    cols_to_add.clear()
    # cols and rows to add
    for c in range(w):
        if len("".join([M[r][c] for r in range(h)]).replace(".", "")) == 0:
            cols_to_add.append(c)

    for r in range(h):
        if len("".join(M[r]).replace(".", "")) == 0:
            rows_to_add.append(r)
    if not is_part2:
        new_M = [["." for _ in range(w + len(cols_to_add))] for _ in range(h + len(rows_to_add))]
    else:
        new_M = [["." for _ in range(w)] for _ in range(h)]

    # expand map
    inc_c = 0
    for c in range(w):
        if c in cols_to_add:
            inc_c += 1 if not is_part2 else 0
        inc_r = 0
        for r in range(h):
            if r in rows_to_add:
                inc_r += 1 if not is_part2 else 0
            ch = M[r][c]
            new_M[r + inc_r][c + inc_c] = ch
            if ch == "#":
                galaxies.append((r + inc_r, c + inc_c))

    print(f"Num galaxies found: {len(galaxies)}")
    return new_M, galaxies


def manhattan_distance(p1, p2, is_part2=False, X=1000000):
    crosses = 0

    def cnt_between(lst, A, B):
        return len([x for x in lst if A < x < B])

    # Calculate the distance in the x direction
    if is_part2:
        crosses += cnt_between(rows_to_add, min(p1[0], p2[0]), max(p1[0], p2[0]))
        crosses += cnt_between(cols_to_add, min(p1[1], p2[1]), max(p1[1], p2[1]))
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) + crosses * X - crosses


def part1_and_2(input):
    # Part 1
    M, galaxies = expand_map(input)
    dist = []
    for p1, p2 in combinations(galaxies, 2):
        dist.append(manhattan_distance(p1, p2))
    print(f"Part 1: all distances {dist}, sum {sum(dist)}")

    # Part 2
    M, galaxies = expand_map(input, is_part2=True)
    dist = []
    for p1, p2 in combinations(galaxies, 2):
        dist.append(manhattan_distance(p1, p2, is_part2=True))
    print(f"Part 2: all distances {dist}, sum {sum(dist)}")
    pass


if __name__ == "__main__":
    part1_and_2(input)
