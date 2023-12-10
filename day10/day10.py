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
year = int(re.search("\\d{4}", cwd).group(0))
day = int(re.search("\\/day(\\d+)", cwd).group(1))
input = open(f"day{day}/input_{year}_{day}.txt", "r").read()
input = [line for line in input.splitlines()]


# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
# . is ground; there is no pipe in this tile.
pipe_dir = {
    "|": ["N", "S"],
    "-": ["E", "W"],
    "L": ["N", "E"],
    "J": ["N", "W"],
    "7": ["S", "W"],
    "F": ["S", "E"],
}
delta_d = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "W": (0, -1)}

# parse input map, and find start position
M = [[ch for ch in row] for row in input]
start_pos = [(r, c) for r in range(len(M)) for c in range(len(M[0])) if M[r][c] == "S"][0]

path = []


def move(pos, dirs, prev_pos):
    orig_pos = pos
    potential = []
    for d in pipe_dir[dirs]:
        potential.append(tuple(map(operator.add, pos, delta_d[d])))
    pos = [p for p in potential if p != prev_pos][0]
    return pos, orig_pos


def part1(input):
    # start right (I looked manually in the map :)
    prev_pos = start_pos
    path.append(start_pos)
    pos = tuple(map(operator.add, prev_pos, delta_d["E"]))
    cnt = 1
    while pos != start_pos:
        path.append(pos)
        pipe = M[pos[0]][pos[1]]
        pos, prev_pos = move(pos, pipe, prev_pos)
        cnt += 1
    return cnt // 2


def part2(input):
    # Shoelace formula
    # https://en.wikipedia.org/wiki/Shoelace_formula
    def shoelace_area(points):
        n = len(points)
        res = 0
        for i in range(n):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % n]
            res += x1 * y2 - x2 * y1
        return abs(res // 2)

    # Pick's theorem
    # https://en.wikipedia.org/wiki/Pick%27s_theorem
    return shoelace_area(path) - part1(input) + 1


if __name__ == "__main__":
    print(f"Part 1: furthest distance {part1(input)}")
    print(f"Part 2: number inside positions {part2(input)}")
