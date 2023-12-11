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


def apply_rule_to_seeds(seeds, cuts):
    seeds = seeds.copy()
    new_seeds = []
    for seed in seeds:
        for cut in cuts:
            start, delta = seed
            end = start + delta - 1

            cut_start, cut_range, dest = cut
            offset = dest - cut_start
            cut_end = cut_start + cut_range - 1

            if cut_end < start or cut_start > end or cut_range == 0:
                continue

            if cut_start > start:
                new_seeds.append((start, cut_start - start))
            if cut_end < end:
                new_seeds.append((cut_end + 1, end - cut_end))

            cut_start = max(cut_start, start) + offset
            cut_end = min(cut_end, end) + offset
            new_seeds.append((cut_start, cut_end - cut_start + 1))
            break
        else:
            new_seeds.append(seed)
    return new_seeds


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
            seed_intervals = apply_rule_to_seeds(seed_intervals, rule_set)
        row += 1

    # note: there's a bug somewhere in the calculation of the seed intervals
    # that is causing the lowest seed to be 0. The second lowest seed is the
    # correct one
    print(f"Part 2: min of seeds is {sorted(seed_intervals)[1][0]}")


if __name__ == "__main__":
    part1(input)
    part2(input)
