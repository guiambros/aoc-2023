import hashlib
import operator
import os
import re
import sys
from collections import defaultdict
from copy import deepcopy
from functools import lru_cache, reduce

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


def rotate_map_clockwise(m):
    return [list(reversed(i)) for i in zip(*m)]


def rotate_map_counterclockwise(m):
    return list(reversed([list(i) for i in zip(*m)]))


def tilt_right(m):
    h = len(m)
    w = len(m[0])

    def move_right(r, c):
        cnt = 0
        max_right = c
        for i in range(c + 1, w):
            if m[r][i] == ".":
                max_right = i
                cnt += 1
            elif m[r][i] in ["#", "O"]:
                break
            else:
                print("error!")
                break
        if cnt:
            m[r][c] = "."
            m[r][max_right] = "O"
            return (r, max_right)
        return None

    for r in range(h):
        for c in range(w - 1, -1, -1):
            if m[r][c] == "O":
                while True:
                    res = move_right(r, c)
                    if res is None:
                        break
                    (r, c) = res
    return m


def calculate_score(m):
    h = len(m)
    w = len(m[0])
    return sum([(h - r) for r in range(h) for c in range(w) if m[r][c] == "O"])


def part1(M):
    # M = rotate_map_clockwise(M)
    # tilt_right(M)
    # M = rotate_map_counterclockwise(M)
    # score = calculate_score(M)
    # print(f"Part 1: {score}")
    # pass
    tilt(M)
    score = calculate_score(M)
    print(f"Part 1: {score}")
    # pass


def tilt(M):
    h = len(M)
    w = len(M[0])
    num_moves = 0

    for r in range(h - 1, 0, -1):
        for c in range(w):
            if M[r][c] == "O" and M[r - 1][c] == ".":
                M[r][c] = "."
                M[r - 1][c] = "O"
                num_moves += 1
    if num_moves:
        tilt(M)
    return M


def tilt_cycle_orig(M, n=1):
    hash_cache = {}
    cycle_cache = {}
    cycle_start, cycle_end = float("inf"), float("-inf")
    cycle = None

    for i in range(4 * n):
        h = hashlib.sha256(str(M).encode()).hexdigest()
        if h in hash_cache:
            print(f"Iteration {i} matches the one seen at {hash_cache[h][0]}")
            cycle, M = hash_cache[h]
            cycle_start = min(cycle_start, cycle)
            cycle_end = max(cycle_end, cycle)
            cycle_cache[cycle - cycle_start] = deepcopy(M)
            if cycle < cycle_end:  # end of the cycle
                print(f"Cycle length is {cycle_end - cycle_start}")
                print(f"Cycle starts at {cycle_start} and ends at {cycle_end}")
                break
        else:
            M = rotate_map_clockwise(M)
            M = tilt_right(M)
            hash_cache[h] = (i, deepcopy(M))

        if i % 10000 == 0:
            print(f"tilt cycle {i}")
    final_cycle = cycle_cache[(n - cycle) % (cycle_end - cycle_start)] if cycle else M
    # M = rotate_map_counterclockwise(final_cycle)
    return M


def tilt_cycle(M, n=1):
    cache = {}
    cycle_cache = {}
    cycle_start, cycle_end = float("inf"), float("-inf")
    cycle = None
    for _ in range(n):
        h = hashlib.sha256(str(M).encode()).hexdigest()
        if h in cache:
            # do something with the cycle
            pass
        else:
            cache[h] = deepcopy(M)
            for _ in range(4):
                M = tilt(M)
                M = rotate_map_clockwise(M)
    return M


def print_map(M):
    print("\n\n")
    for row in M:
        print("".join(row))


def part2(M):
    M = tilt_cycle(M, 1000000000)
    # M = tilt_cycle(M, 3)
    score = calculate_score(M)
    # print(f"Map:\n{M}\n\n")
    # print(["".join(row) for row in M])
    print(f"Part 2: {score}")
    pass


M = [list(line) for line in input]

if __name__ == "__main__":
    part1(deepcopy(M))
    part2(deepcopy(M))
