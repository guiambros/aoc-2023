import operator
import os
import re
import sys
from collections import defaultdict
from copy import deepcopy
from functools import reduce

import sol

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


def read_input(input):
    M = {}
    mirror = 1
    this_mirror = []
    for line in input:
        if len(line) < 2:
            M[mirror] = this_mirror
            this_mirror = []
            mirror += 1
            continue
        this_mirror.append(list(line))
    return M


def scan_horizontal(mirror):
    return scan_vertical(mirror, ishorizontal=True)


def scan_vertical(mirror, ishorizontal=False):
    if ishorizontal:
        w = len(mirror)
        h = len(mirror[0])
    else:
        h = len(mirror)
        w = len(mirror[0])

    for i in range(w):
        # check if immediate columns are the same
        _this = i
        _next = (i + 1) % w
        if ishorizontal:
            c1 = mirror[_this]
            c2 = mirror[_next]
        else:
            c1 = [row[_this] for row in mirror]
            c2 = [row[_next] for row in mirror]
        if c1 != c2:
            continue

        is_palindrome = True
        for j in range(1, (w - 1) // 2):
            _next = (i + j + 1) % w
            _prev = (i - j) % w
            if ishorizontal:
                c1 = mirror[_next]
                c2 = mirror[_prev]
            else:
                c1 = [row[_next] for row in mirror]
                c2 = [row[_prev] for row in mirror]
            if c1 != c2:
                is_palindrome = False
                break
        if is_palindrome:
            return i
    return None


def part1(input):
    M = read_input(input)
    total = 0
    for id, mirror in M.items():
        row = scan_horizontal(mirror)
        col = scan_vertical(mirror)
        if row:
            print(f"Mirror {id} found horizontal at row {row+1}")
        if col:
            print(f"Mirror {id} Found vertical at col {col+1}")
        total += (col + 1 if col else 0) + 100 * (row + 1 if row else 0)

    print(f"Part 1: {total}")
    pass


def part2(input):
    print(f"Part 2: {None}")
    pass


if __name__ == "__main__":
    part1(input)
    part2(input)
