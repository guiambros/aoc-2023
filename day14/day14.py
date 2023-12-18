import hashlib
import re
import sys
import time
from copy import deepcopy
from functools import cache, lru_cache, reduce


def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} took {end_time - start_time} seconds to run.")
        return result

    return wrapper


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


def calculate_score(m):
    h = len(m)
    w = len(m[0])
    return sum([(h - r) for r in range(h) for c in range(w) if m[r][c] == "O"])


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


def tilt_cycle(M, n=1):
    i, M_cache = 0, {}
    cache_ptr, cycle_start, cycle_end = 0, float("inf"), float("-inf")
    cycle_detection = True

    while i < n:
        h = hashlib.sha256(str(M).encode()).hexdigest()
        if h in M_cache:
            ptr = M_cache[h][0]
            # print(f"\nIteration {i} matches the one seen at {ptr} -- {h}")
            cycle_start = min(cycle_start, ptr)
            cycle_end = max(cycle_end, ptr)
            cycle_length = cycle_end - cycle_start + 1
            if cycle_detection and ptr == cycle_start and cycle_end > cycle_start:
                print(
                    f"Found pattern; cycle starts at {cycle_start}, ends at {cycle_end}, length {cycle_length}"
                )
                cycle_detection = False
                i += ((n - i) // cycle_length) * cycle_length - 1  # skip to the end of the cycle
            else:
                M = M_cache[h][1]
        else:
            M_input = deepcopy(M)
            for _ in range(4):
                M = tilt(M)
                M = rotate_map_clockwise(M)
            h = hashlib.sha256(str(M_input).encode()).hexdigest()
            M_cache[h] = (cache_ptr, deepcopy(M))  # cache ptr, input, output
            cache_ptr += 1
        # print(f"After rotation {i}: {hashlib.sha256(str(M).encode()).hexdigest()}")
        i += 1

    return M


def print_map(M):
    print("\n\n")
    for row in M:
        print("".join(row))


@timer
def part1(M):
    tilt(M)
    score = calculate_score(M)
    print(f"Part 1: {score}")


@timer
def part2(M):
    M = tilt_cycle(M, 1000000000)
    score = calculate_score(M)
    print(f"Part 2: {score}")


M = [list(line) for line in input]

if __name__ == "__main__":
    part1(deepcopy(M))
    part2(deepcopy(M))
