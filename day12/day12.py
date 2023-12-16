import operator
import os
import re
import sys
import time
from collections import defaultdict
from copy import deepcopy
from functools import cache, lru_cache, reduce

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
M = [(line.split(" ")[0], line.split(" ")[1]) for line in input]


@cache
def get_block(breakdown_str):
    return breakdown_str.split(",")


@cache
def is_valid(s, breakdown):
    def count_blocks(s):
        s = s.strip(".") + "."
        blocks = []
        in_block = True
        block_cnt = 0
        for i, c in enumerate(s):
            if c == "#":
                block_cnt += 1
                in_block = True
            elif in_block == True:
                blocks.append(block_cnt)
                block_cnt = 0
                in_block = False
        return blocks

    return tuple(count_blocks(s)) == breakdown


@cache
def fuzz(s, size):
    combinations = []
    if len(s) == size and s.find("?") == -1:
        return [s]
    i = s.find("?")
    s = s[:i] + "#" + s[i + 1 :]
    combinations += fuzz(s, size)
    s = s[:i] + "." + s[i + 1 :]
    combinations += fuzz(s, size)
    return combinations


@cache
def cnt_valid_combinations(s, breakdown):
    combinations = fuzz(s, len(s))
    valid_combinations = 0
    for c in combinations:
        if is_valid(c, breakdown):
            valid_combinations += 1
    return valid_combinations


def part1(input):
    valid_combinations = []
    for i, (s, breakdown) in enumerate(M):
        breakdown = tuple([int(b) for b in breakdown.split(",")])
        valid_combinations.append(cnt_valid_combinations(s, breakdown))
        print(f"{i}: {s} ({breakdown}) = {valid_combinations[-1]}")

    print(f"Part 1: {sum(valid_combinations)}")


def part2(input):
    print(f"Part 2: {None}")
    pass


if __name__ == "__main__":
    start_time = time.time()
    part1(input)
    print(f"Execution time: {time.time() - start_time}\n")

    start_time = time.time()
    part2(input)
    print(f"Execution time: {time.time() - start_time}\n")
