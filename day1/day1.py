import operator
import os
import re
import sys
from collections import defaultdict
from copy import deepcopy
from functools import reduce

from PIL import Image

# get current day
cwd = sys.argv[0]
if not ("day" in cwd):
    print("Run this from the day directory")
    sys.exit(0)

# read input data
year = int(re.search("\\d{4}", cwd).group(0))
day = int(re.search("\\/day(\\d+)", cwd).group(1))


file_input = open(f"day{day}/input_{year}_{day}.txt", "r").read()
# input = open(f"day{day}/input_{year}_{day}_test.txt", "r").read()
raw_input = file_input.splitlines()

# input in a single line
# input = [line for line in input.split(",")]
# input = [int(i) for i in input]


def part1(input):
    total = 0
    for l in input:
        digits = [c for c in l if c.isdigit()]
        total += int(digits[0] + digits[-1])
    print(total)


def find_digit(l, d, reverse=False):
    range_ = range(len(l), -1, -1) if reverse else range(len(l) + 1)

    # find first digit
    for i in range_:
        substr = l[i:] if reverse else l[:i]
        digit = next((int(ch) for ch in substr if ch.isdigit()), False)
        if not digit:
            digit = next((v for k, v in d.items() if k in substr), False)
        if digit:
            return digit
    return False


def part2(input):
    total = 0
    d = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }
    for line in input:
        first = find_digit(line, d)
        last = find_digit(line, d, True)
        total += int(str(first) + str(last or first))
        # print(line, first, last)
    print(total)


if __name__ == "__main__":
    # part1(raw_input)
    part2(raw_input)
