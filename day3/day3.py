import math as m
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
input = [line for line in input.splitlines()]

# input in a single line
# input = [line for line in input.split(",")]

# convert list to int
# input = [int(i) for i in input]


def get_number(input, row, col):
    number = []
    coords = []

    # find the starting position of the number
    while col >= 1 and input[row][col - 1].isdigit():
        col -= 1

    # get the full number
    while col < len(input[row]) and input[row][col].isdigit():
        number.append(input[row][col])
        coords.append((row, col))
        col += 1

    return int("".join(number)), coords


# check if there's a symbol somewhere close to this digit
def check_if_valid_number(input, row, col, is_part2=False):
    coords = [
        (row - 1, col - 1),
        (row - 1, col),
        (row - 1, col + 1),
        (row, col - 1),
        (row, col + 1),
        (row + 1, col - 1),
        (row + 1, col),
        (row + 1, col + 1),
    ]
    for r, c in coords:
        if r >= 0 and r < len(input) and c >= 0 and c < len(input[r]):
            ch = input[r][c]
            if not is_part2 and not ch.isdigit() and ch != ".":
                return True
            elif is_part2 and ch == "*":
                return True
    return False


def find_nearby_numbers(input, row, col):
    numbers = []
    coords_processed = []
    delta_coords = [
        (row - 1, col - 1),
        (row - 1, col),
        (row - 1, col + 1),
        (row, col - 1),
        (row, col + 1),
        (row + 1, col - 1),
        (row + 1, col),
        (row + 1, col + 1),
    ]
    for r, c in delta_coords:
        if r >= 0 and r < len(input) and c >= 0 and c < len(input[r]):
            ch = input[r][c]
            if ch.isdigit() and (r, c) not in coords_processed:
                num, coords = get_number(input, r, c)
                coords_processed += coords
                numbers.append(num)
    return numbers


def part1(input):
    numbers = []
    for row, l in enumerate(input):
        decoding_number = False
        valid_number = False
        number = None
        for col, ch in enumerate(l):
            if ch.isdigit():
                if not decoding_number:  # get the full number on the first digit found
                    number, _ = get_number(input, row, col)
                    decoding_number = True

                if not valid_number:  # check if there's a symbol somewhere close to this digit
                    if check_if_valid_number(input, row, col):
                        numbers.append(number)
                        valid_number = True
            else:
                decoding_number = False
                valid_number = False
                number = None
    print(f"Part 1: total sum of valid numbers {sum(numbers)}")


def part2(input):
    numbers = []
    gears = []
    for row, l in enumerate(input):
        for col, ch in enumerate(l):
            if ch == "*":
                numbers = find_nearby_numbers(input, row, col)
                if len(numbers) == 2:
                    gears.append(numbers[0] * numbers[1])
    print(f"Part 2: total sum of gears multiplied {sum(gears)}")


def solution(input):
    board = list(input)
    chars = {
        (r, c): [] for r in range(140) for c in range(140) if board[r][c] not in "01234566789."
    }

    for r, row in enumerate(board):
        for n in re.finditer(r"\d+", row):
            edge = {(r, c) for r in (r - 1, r, r + 1) for c in range(n.start() - 1, n.end() + 1)}

            for o in edge & chars.keys():
                chars[o].append(int(n.group()))

    print(
        sum(sum(p) for p in chars.values()), sum(m.prod(p) for p in chars.values() if len(p) == 2)
    )


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
