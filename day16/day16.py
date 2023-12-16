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
M = [[ch for ch in row] for row in input]
h = len(M)
w = len(M[0])

pos, dir = {}, {}
pos = (0, 0)
dir = "E"
energized = set()
num_beams = 1
reflected_beams = []


def reflect_beam(pos, dir):
    if (pos, dir) in reflected_beams:
        print("already reflected beam", pos, dir)
        return
    reflected_beams.append((pos, dir))
    print("reflecting beam", pos, dir)

    while True:
        r, c = pos

        # beam out of bounds
        if r < 0 or r >= h or c < 0 or c >= w:
            break

        ch = M[r][c]
        energized.add((r, c))
        if ch == ".":
            pass
        elif ch == "/":
            if dir == "E":
                dir = "N"
            elif dir == "W":
                dir = "S"
            elif dir == "N":
                dir = "E"
            elif dir == "S":
                dir = "W"
        elif ch == "\\":
            if dir == "E":
                dir = "S"
            elif dir == "W":
                dir = "N"
            elif dir == "N":
                dir = "W"
            elif dir == "S":
                dir = "E"
        elif (ch == "-" and dir in ["E", "W"]) or (M[r][c] == "|" and dir in ["N", "S"]):
            pass
        elif (ch == "-" and dir in ["S", "N"]) or (M[r][c] == "|" and dir in ["E", "W"]):
            # split beams
            new_dirs = split_beam_dir(dir)
            # map(lambda x: reflect_beam(pos, x), new_dirs)
            reflect_beam(pos, new_dirs[0])
            reflect_beam(pos, new_dirs[1])
            break

        # move beams forward
        pos, dir = move_beam(pos, dir)


def split_beam_dir(dir):
    # M[r][c] == "-" and dir in ["S", "N"] or M[r][c] == "|" and dir in ["E", "W"]:
    if dir in ["E", "W"]:
        return ["N", "S"]
    elif dir in ["N", "S"]:
        return ["E", "W"]
    else:
        raise ValueError(f"Invalid direction: {dir}")


def move_beam(pos, dir):
    GPS = {"E": (0, 1), "W": (0, -1), "N": (-1, 0), "S": (1, 0)}
    new_pos = (pos[0] + GPS[dir][0], pos[1] + GPS[dir][1])
    return new_pos, dir


def part1(input):
    reflect_beam(pos, dir)
    print(f"Part 1: {len(energized)}\n\n")
    for r in range(len(M)):
        for c in range(len(M[0])):
            if (r, c) in energized and M[r][c] == ".":
                ch = "#"
            else:
                ch = M[r][c]
            print(ch, end="")
        print("")
    pass


def part2(input):
    print(f"Part 2: {None}")
    pass


if __name__ == "__main__":
    part1(input)
    part2(input)
