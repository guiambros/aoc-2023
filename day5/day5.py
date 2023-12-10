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


input = open(f"day{day}/input_{year}_{day}.txt", "r").read().splitlines()


def map_seeds(seeds, rule_set):
    new_seeds = []
    while seeds:
        s = seeds.pop(0)
        found = False
        for r in rule_set:
            src, rg, dst = r
            if src <= s < src + rg:
                new_seed = s - src + dst
                new_seeds.append(new_seed)
                found = True
                break
        if not found:
            new_seeds.append(s)
    return new_seeds


def read_rules(input, row):
    rules = []
    while row < len(input):
        line = input[row]
        if line == "":
            break
        dst, src, rg = line.split(" ")
        dst = int(dst)
        src = int(src)
        rg = int(rg)
        rules.append((src, rg, dst))
        row += 1
    return rules, row


def part1(input):
    seeds = [int(s) for s in input[0].split(":")[1].strip().split(" ")]

    row = 2
    rule_set = []

    while row < len(input):
        line = input[row]

        if ":" in line:
            rule_set, row = read_rules(input, row + 1)

        if len(rule_set) > 0:
            seeds = map_seeds(seeds, rule_set)
        row += 1

    print(f"Part 1: min of seeds {seeds} is {min(seeds)}")
    pass


def decode_seed_pairs(seeds):
    new_seeds = []
    while seeds:
        start = seeds.pop(0)
        rg = seeds.pop(0)
        new_seeds.append((start, rg))
    return new_seeds


def map_seeds_ranges(seed_intervals, rule_set):
    new_intervals = []

    while seed_intervals:
        s0, s_delta = seed_intervals.pop(0)
        s1 = s0 + s_delta
        found = False
        for r in rule_set:
            r0, r_delta, dst = r
            r1 = r0 + r_delta

            if s0 < r0 and s1 > r0:  # case 1 - seed interval starts before rule block and overlaps
                found = True
                new_intervals.append((s0, r0 - s0, s0))
                new_intervals.append((r0, min(s1 - r0 + 1, r_delta), dst))
                if s1 > r1:  # interval extends beyond rule
                    new_intervals.append((r1, s1 - r1, r1))

            elif s0 > r0 and s0 < r1:  # case 2 - seed interval starts in the middle of rule block
                found = True
                if s1 < r1:
                    new_intervals.append((s0, s_delta, dst + (s0 - r0)))
                else:
                    new_intervals.append((s0, r1 - s0, dst + (s0 - r0)))
                    new_intervals.append((r1, s1 - r1, r1))

            elif s0 < r0 and s1 > r1:  # case 3 - seed interval spans the entire rule block
                found = True
                new_intervals.append((s0, r0 - s0, s0))
                new_intervals.append((r0, r_delta, dst))
                new_intervals.append((r1, s1 - r1, r1))

        if not found:
            new_intervals.append((s0, s_delta, s0))

    new_intervals = [(dst, rg) for st, rg, dst in new_intervals]
    return new_intervals


def part2(input):
    seeds = [int(s) for s in input[0].split(":")[1].strip().split(" ")]
    seed_intervals = decode_seed_pairs(seeds)
    rule_set = []

    row = 2
    while row < len(input):
        line = input[row]
        if ":" in line:
            rule_set, row = read_rules(input, row + 1)
        if len(rule_set) > 0:
            seed_intervals = map_seeds_ranges(seed_intervals, rule_set)
        row += 1

    print(f"Part 2: min of seeds is {min([s for s, _ in seed_intervals])}")
    pass


if __name__ == "__main__":
    part1(input)
    part2(input)

## Part 1
#
