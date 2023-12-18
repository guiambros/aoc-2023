import operator
import os
import re
import sys
from collections import defaultdict
from copy import deepcopy
from functools import cache, lru_cache, reduce
import time


def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} took {end_time - start_time} seconds to run.")
        return result

    return wrapper


# get current day from path and read input data
cwd = sys.argv[0]
if not ("day" in cwd):
    print("Run this from the day directory")
    sys.exit(0)
year = int(re.search("\\d{4}", cwd).group(0))
day = int(re.search("\\/day(\\d+)", cwd).group(1))
input = open(f"day{day}/input_{year}_{day}.txt", "r").read()


def part1(input):
    print(f"Part 1: {None}")
    pass


def part2(input):
    print(f"Part 2: {None}")
    pass


if __name__ == "__main__":
    # -- input in multiple lines
    # input = [line for line in input.splitlines()]

    # -- convert multi-line elements to int
    # input = [[int(c) for c in row.split(" ")] for row in input]

    # -- input in a single line
    # input = [line for line in input.split(",")]

    # -- convert single line list to int
    # input = [int(i) for i in input]

    part1(input)
    part2(input)
