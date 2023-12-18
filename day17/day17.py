import heapq
import operator
import re
import sys

# get current day
cwd = sys.argv[0]
if not ("day" in cwd):
    print("Run this from the day directory")
    sys.exit(0)

# read input data
year = int(re.search("\\d{4}", cwd).group(0))
day = int(re.search("\\/day(\\d+)", cwd).group(1))


def dijkstra(M, start, dest, at_least=1, at_most=3):
    # inspired by u/xelf's comments here:
    # https://www.reddit.com/r/adventofcode/comments/18k9ne5/comment/kdq86mr/
    h, w, tick = len(M), len(M[0]), 0
    Q = [(0, start, [start], (0, 0))]
    visited = set()

    while Q:
        tick += 1
        cost, pos, path, dir = heapq.heappop(Q)

        if pos == dest:
            print(f"Destination reached in {tick} steps; queue len = {len(Q)}")
            return cost, path

        if (pos, dir) in visited:
            continue

        visited.add((pos, dir))
        dirs = {(1, 0), (0, 1), (-1, 0), (0, -1)} - {(dir[0], dir[1]), (-dir[0], -dir[1])}
        for d in dirs:
            new_pos, new_cost = pos, cost
            for i in range(1, at_most + 1):
                new_pos = tuple(map(operator.add, new_pos, d))
                if 0 <= new_pos[0] < h and 0 <= new_pos[1] < w:  # if we're still on the board
                    new_cost += M[new_pos[0]][new_pos[1]]
                    path += [new_pos]
                    if i >= at_least:
                        heapq.heappush(Q, (new_cost, new_pos, path + [new_pos], d))
    return float("inf"), []  # destination is unreachable


def print_map(M, path):
    h, w = len(M), len(M[0])
    for r in range(h):
        for c in range(w):
            if (r, c) in path:
                print("*", end="")
            else:
                print(M[r][c], end="")
        print()
    print()


def part1_and_2(M):
    best_cost1, path = dijkstra(M, (0, 0), (h - 1, w - 1))
    print("\n\nPart 1 --- map\n")
    print_map(M, path)

    # pt2
    best_cost2, path = dijkstra(M, (0, 0), (h - 1, w - 1), 4, 10)
    print("\n\nPart 2 --- map\n")
    print_map(M, path)
    print(f"Part 1: {best_cost1}")
    print(f"Part 2: {best_cost2}")


if __name__ == "__main__":
    input = open(f"day{day}/input_{year}_{day}.txt", "r").read()
    input = [[int(ch) for ch in row] for row in input.splitlines()]
    h, w = len(input), len(input[0])
    part1_and_2(input)
