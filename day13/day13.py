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


def read_input(input):
    def rotate(mirror):
        return ["".join([mirror[j][i] for j in range(len(mirror))]) for i in range(len(mirror[0]))]

    def to_bin(m):
        return [sum(2**i if c == "#" else 0 for i, c in enumerate(row)) for row in m]

    Mr, Mc, this_mirror = [], [], []
    while input:
        line = input.pop(0)
        if len(line) == 0:
            Mr.append(to_bin(this_mirror))
            Mc.append(to_bin(rotate(this_mirror)))
            this_mirror = []
            continue
        this_mirror.append(line)
    Mr.append(to_bin(this_mirror))
    Mc.append(to_bin(rotate(this_mirror)))
    return Mr, Mc


def find_mirror(M):
    i = 1
    found = []
    while i < len(M):
        if M[i] == M[i - 1]:
            next = [M[i + delta] == M[i - delta - 1] for delta in range(1, min(i, len(M) - i))]
            if all(next):
                found.append(i)
        i += 1
    return found


def part1():
    Rr, Rc = defaultdict(lambda: None), defaultdict(lambda: None)

    score = 0
    for num, M in enumerate(Mr):
        pos = find_mirror(M)
        if len(pos) > 1:
            raise Exception(f"Found multiple mirrors for pattern {num}: {pos}")
        elif len(pos) == 1:
            Rr[num] = pos[0]
            score += pos[0] * 100

    for num, M in enumerate(Mc):
        pos = find_mirror(M)
        if len(pos) > 1:
            raise Exception(f"Found multiple mirrors for pattern {num}: {pos}")
        elif len(pos) == 1:
            Rc[num] = pos[0]
            score += pos[0]

    print(f"Part 1: {score}")
    return Rr, Rc


def part2(Rr, Rc):
    def count_bit_flips(a, b):
        return bin(a ^ b).count("1")

    new_reflections = dict()
    for num, M in enumerate(Mr):
        for i in range(len(M)):
            for j in range(i + 1, len(M)):
                if count_bit_flips(M[i], M[j]) == 1:
                    # try changing the smudge to # or . and see if the reflection changes
                    opt = list(M)
                    opt[j] = M[i]
                    for pos in find_mirror(opt):
                        if pos != Rr[num]:
                            print(
                                f"Found smudge pat {num} - bit flip row {i} ({M[i]}) and {j} ({M[j]}) -- mirror pos {pos}"
                            )
                            new_reflections[num] = pos
                            break
    score = sum([pos * 100 for pos in new_reflections.values()])

    new_reflections = dict()
    for num, M in enumerate(Mc):
        for i in range(len(M)):
            for j in range(i + 1, len(M)):
                if count_bit_flips(M[i], M[j]) == 1:
                    # try changing the smudge to # or . and see if the reflection changes
                    opt = list(M)
                    opt[j] = M[i]
                    for pos in find_mirror(opt):
                        if pos != Rc[num]:
                            print(
                                f"Found smudge pat {num} - bit flip col {i} ({M[i]}) and {j} ({M[j]}) -- mirror pos {pos}"
                            )
                            new_reflections[num] = pos
                            break
    score += sum([pos for pos in new_reflections.values()])

    print(f"Part 2: {score}")
    # assert score == 23479
    pass


if __name__ == "__main__":
    Mr, Mc = read_input(input)
    Rr, Rc = part1()
    part2(Rr, Rc)
