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
# input = open(f"day{day}/input_{year}_{day}_test.txt", "r").read()

# input in multiple lines
# input = [line for line in input.splitlines()]

# input in a single line
# input = [line for line in input.split(",")]

# convert list to int
# input = [int(i) for i in input]


def part1(input):
    print(f"Part 1: {None}")
    pass


def part2(input):
    print(f"Part 2: {None}")
    pass


if __name__ == "__main__":
    part1(input)
    part2(input)

# Example of an input that requires regex parsing
# Format:
#   kvlbq (22)
#   rdrad (6) -> gwyfm, fozyip, uotzz, fmkkz
#   oqbfkud (470) -> rnbqhk, mepez, mnksdxf, mjsck, bbfaxid, nglea
#   zzjyw (91)
#
# t = dict( \
#    (m[0], (int(m[1]), m[3].split(", ") if m[3] else [])) \
#       for m in [re.match("(\w+) \((\d+)\)( -> ((\w+, )*\w+))?", l).groups() \
#       for l in d] \
# )
