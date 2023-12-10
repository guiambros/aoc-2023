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

GPS = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "W": (0, -1)}
pipe_dir = {
    "|": ["N", "S"],
    "-": ["E", "W"],
    "L": ["N", "E"],
    "J": ["N", "W"],
    "7": ["S", "W"],
    "F": ["S", "E"],
}
M = [[ch for ch in row] for row in input]
start_pos = [(r, c) for r in range(len(M)) for c in range(len(M[0])) if M[r][c] == "S"][0]


def move(pos, dirs, prev_pos):
    orig_pos = pos
    potential = []
    for d in pipe_dir[dirs]:
        potential.append(tuple(map(operator.add, pos, GPS[d])))
    pos = [p for p in potential if p != prev_pos][0]
    return pos, orig_pos


def part1(input):
    # start right (I looked manually in the map :)
    prev_pos = start_pos
    pos = tuple(map(operator.add, prev_pos, GPS["E"]))
    cnt = 1
    while pos != start_pos:
        pipe = M[pos[0]][pos[1]]
        pos, prev_pos = move(pos, pipe, prev_pos)
        cnt += 1

    print(f"Part 1: size pipes {cnt}, furthest distance {cnt//2}")


def part2(input):
    print(f"Part 2: {None}")
    pass


if __name__ == "__main__":
    part1(input)
    part2(input)
