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
    # for cut in cuts:
    #   start, length, dest = cut
    #   offset = dest - start
    #   seeds = cut_intervals(seeds, (start, length), offset)
    # ---

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


def cut_intervals(original_intervals, cut_range, offset):
    new_intervals = []
    for original_interval in original_intervals:
        new_intervals.extend(cut_interval(original_interval, cut_range, offset))
    return new_intervals


def cut_interval(interval, cut, offset):
    start, delta = interval
    end = start + delta - 1

    cut_start, cut_range = cut
    cut_end = cut_start + cut_range - 1

    if cut_end < start or cut_start > end:
        return [interval]

    new_intervals = []
    if cut_start > start:
        new_intervals.append((start, cut_start - start))
    if cut_end < end:
        new_intervals.append((cut_end + 1, end - cut_end))

    cut_start = max(cut_start, start) + offset
    cut_end = min(cut_end, end) + offset
    new_intervals.append((cut_start, cut_end - cut_start + 1))

    return new_intervals


def consolidate_intervals(intervals):
    if not intervals:
        return []

    # Sort intervals based on start values
    intervals.sort(key=lambda x: x[0])

    consolidated = [intervals[0]]

    for current in intervals[1:]:
        last = consolidated[-1]

        # If the current interval does not overlap with the last, append it
        if current[0] > last[1]:
            consolidated.append(current)
        else:
            # Otherwise, there is overlap, so we merge the current and last interval
            consolidated[-1] = (last[0], max(last[1], current[1]))

    return consolidated


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
        # print(f"Row {row}  seed intervals {seed_intervals}")

    # print(f"Seed intervals {seed_intervals}")
    print(f"Part 2: min of seeds is {min([s for s, _ in seed_intervals])}")
    pass
    # answer:  15290096
    #         481035699
    # problematic lowest correct: 121383180
    #                        01: (153834827, 16551754)

    # all_destinations
    # (0, 30744318), (2036192302, 2060857942)
    #
    # new_seeds
    # (0, 30744319), (878508582, 24665641)


if __name__ == "__main__":
    # part1(input)
    part2(input)

## Part 1
#
