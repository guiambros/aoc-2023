import re
import sys
import time
from functools import cache
from multiprocessing import Pool

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


def get_block(breakdown_str):
    return breakdown_str.split(",")


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


def num_valid_solutions_bruteforce(s, breakdown):
    combinations = fuzz(s, len(s))
    valid_combinations = 0
    for c in combinations:
        if is_valid(c, breakdown):
            valid_combinations += 1
    return valid_combinations


def solve_bruteforce(i):
    (s, breakdown) = M[i]
    breakdown = tuple([int(b) for b in breakdown.split(",")])
    valid_combinations = num_valid_solutions_bruteforce(s, breakdown)
    # print(f"{i}: {s} ({breakdown}) = {valid_combinations}")
    return valid_combinations


@cache
def num_valid_solutions(s, groups):
    # inspired by reddit comment by u/damaltor1 and @xavdid
    # https://reddit.com/r/adventofcode/comments/18ghux0/2023_day_12_no_idea_how_to_start_with_this_puzzle/kd0npmi/
    # https://advent-of-code.xavd.id/writeups/2023/day/12/

    # if we got to the end of the line and no more blocks to check
    # return 1 if we have a valid solution, 0 otherwise
    if not s:
        return 1 if len(groups) == 0 else 0

    # if we still have blocks to check, make sure there's no more '#'
    if not groups:
        return 1 if "#" not in s else 0

    # if it starts with a ., discard the . and recursively check again.
    if s[0] == ".":
        return num_valid_solutions(s[1:], groups)

    # if it starts with a ?, replace the ? with a . and recursively check again, AND replace it with a # and recursively check again.
    if s[0] == "?":
        return num_valid_solutions("#" + s[1:], groups) + num_valid_solutions("." + s[1:], groups)

    # it it starts with a #, check if it is long enough for the first group, check if all characters in the first [grouplength]
    # characters are not '.', and then remove the first [grouplength] chars and the first group number, recursively check again.
    if s[0] == "#":
        if (
            len(s) < groups[0]  # not enough characters left
            or "." in s[: groups[0]]  # . breaks the sequence
            or (len(s) > groups[0] and s[groups[0]] == "#")  # group would be too big
        ):
            return 0

        return num_valid_solutions(s[groups[0] + 1 :], groups[1:])
    raise Exception("Invalid character {s[0]}")


def solve(i, p2=False):
    (s, breakdown) = M[i]
    if p2:
        s = ((s + "?") * 5)[:-1]
        breakdown = ((breakdown + ",") * 5).strip(",")
    breakdown = tuple([int(b) for b in breakdown.split(",")])
    valid_combinations = num_valid_solutions(s, breakdown)
    # print(f"{i}: {s} ({breakdown}) = {valid_combinations}")
    return valid_combinations


def solve_pt2(i):
    return solve(i, p2=True)


def part1_bruteforce():
    total = sum(map(solve_bruteforce, range(len(M))))
    print(f"Part 1 (brute force, no parallel processing): {total}")


def part1():
    total = 0
    with Pool() as p:
        total += sum(p.map(solve, range(len(M))))
    print(f"Part 1 (recursive with dp, parallel processing): {total}")


def part2():
    total = 0
    with Pool() as p:
        total += sum(p.map(solve_pt2, range(len(M))))
    print(f"Part 2: {total}")


if __name__ == "__main__":
    # part1 via brute force
    # start_time = time.time()
    # part1_bruteforce()
    # print(f"Execution time: {time.time() - start_time}\n")

    # part1 via dp and parallel processing
    start_time = time.time()
    part1()
    print(f"Execution time: {time.time() - start_time}\n")

    # part2 via recursion
    start_time = time.time()
    part2()
    print(f"Execution time: {time.time() - start_time}\n")
    pass
