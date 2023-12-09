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

# input in multiple lines
input = [line for line in input.splitlines()]
input = [[int(c) for c in row.split(" ")] for row in input]


def part1_and_2(input):
    def concat(lst):
        lst = lst.copy()
        for i in range(len(lst) - 1, 0, -1):
            lst[i - 1] -= lst[i]
        return lst[0]

    all_last_nums, all_first_nums = [], []
    for line in input:
        deltas, last_nums, first_nums = [1], [line[-1]], [line[0]]
        while not all([d == 0 for d in deltas]):
            deltas = [j - i for i, j in zip(line[:-1], line[1:])]
            first_nums.append(deltas[0])
            last_nums.append(deltas[-1])
            line = deltas
        all_last_nums.append(sum(last_nums))
        all_first_nums.append(concat(first_nums))
    print(f"Part 1: {sum(all_last_nums)}")
    print(f"Part 2: {sum(all_first_nums)}")


if __name__ == "__main__":
    part1_and_2(input)
