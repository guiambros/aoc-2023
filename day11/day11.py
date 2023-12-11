import re
import sys
from itertools import combinations

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
input = [[ch for ch in input[x]] for x in range(len(input))]
h = len(input)
w = len(input[0])
rows_to_add, cols_to_add = [], []


def map_galaxies(M):
    galaxies = []
    rows_to_add.clear()
    cols_to_add.clear()

    # find empty rows and cols
    for c in range(w):
        if len("".join([M[r][c] for r in range(h)]).replace(".", "")) == 0:
            cols_to_add.append(c)
    for r in range(h):
        if len("".join(M[r]).replace(".", "")) == 0:
            rows_to_add.append(r)

    galaxies = [(r, c) for c in range(w) for r in range(h) if M[r][c] == "#"]
    return galaxies


def manhattan_distance(p1, p2, X=1):
    crosses = 0

    def crosses_between(lst, A, B):
        return len([x for x in lst if A < x < B])

    # Calculate the distance in the x direction
    crosses += crosses_between(rows_to_add, min(p1[0], p2[0]), max(p1[0], p2[0]))
    crosses += crosses_between(cols_to_add, min(p1[1], p2[1]), max(p1[1], p2[1]))
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) + crosses * (X - 1)


def part1_and_2(input):
    # Part 1
    galaxies = map_galaxies(input)
    print(f"Num galaxies found: {len(galaxies)}")

    dist = []
    for p1, p2 in combinations(galaxies, 2):
        dist.append(manhattan_distance(p1, p2, X=2))
    print(f"Part 1: sum {sum(dist)}")

    # Part 2
    dist = []
    for p1, p2 in combinations(galaxies, 2):
        dist.append(manhattan_distance(p1, p2, X=1000000))
    print(f"Part 2: sum {sum(dist)}")


if __name__ == "__main__":
    part1_and_2(input)
