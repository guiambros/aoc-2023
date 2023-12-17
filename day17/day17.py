import heapq
import math
import operator
import re
import sys
from queue import PriorityQueue

# get current day
cwd = sys.argv[0]
if not ("day" in cwd):
    print("Run this from the day directory")
    sys.exit(0)

# read input data
year = int(re.search("\\d{4}", cwd).group(0))
day = int(re.search("\\/day(\\d+)", cwd).group(1))


def search(M, pos, dest, prev_dirs=None, dir=None, visited=None, cost=0):
    prev_dirs = [] if prev_dirs is None else prev_dirs
    visited = [] if visited is None else visited
    dirs = []
    Q = []
    Q.append((pos, prev_dirs, dir, cost))
    best_cost = math.inf

    while len(Q) > 0:
        pos, prev_dirs, dir, cost = Q.pop(0)
        visited.append((pos, prev_dirs, dir))
        this_cost = M[pos[0]][pos[1]]

        if pos == dest:  # we found it!
            if cost < best_cost:
                best_cost = cost
            else:
                continue

        # check possible directions: no reversing direction
        if dir is None:
            dirs = ["E", "S"]
        else:
            if dir in ["E", "W"]:
                dirs = [dir, "N", "S"]
            elif dir in ["N", "S"]:
                dirs = [dir, "E", "W"]
            if prev_dirs.count(dir) >= 2:
                dirs.remove(dir)

        neighbors = []
        for d in dirs:
            # make sure all tentative directions are viable
            c = tuple(map(operator.add, pos, GPS[d]))
            if c[0] < 0 or c[0] >= h or c[1] < 0 or c[1] >= w:
                continue
            _ = prev_dirs[:]
            _.append(d)
            if (c, _[-2:], d) not in visited:
                neighbors.append((c, _[-2:], d, cost + this_cost))

        Q.extend(neighbors)
        # print(len(Q))
    return best_cost


GPS = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "W": (0, -1)}
reverse = {"N": "S", "S": "N", "E": "W", "W": "E"}


def dijkstra3(board, M, start, dest):
    tick = 0
    h, w = len(M), len(M[0])
    Q = []
    Q = [(0, start, [start], (0, 0))]
    visited = set()

    while Q:
        tick += 1
        cost, pos, path, dir = heapq.heappop(Q)

        if pos == dest:
            return cost, path  # return the cost and the path

        if (pos, dir) in visited:
            continue

        visited.add((pos, dir))
        px, py = dir
        dirs = {(1, 0), (0, 1), (-1, 0), (0, -1)} - {(px, py), (-px, -py)}
        for d in dirs:
            new_cost = cost

            # enter 4-10 moves in the chosen direction
            for i in range(1, 3 + 1):
                new_pos = tuple(map(operator.add, pos, d))
                a, b = new_pos
                if (a, b) not in board:
                    continue
                if 0 <= new_pos[0] < h and 0 <= new_pos[1] < w:
                    new_cost += M[new_pos[0]][new_pos[1]]
                    if i >= 1:
                        heapq.heappush(Q, (new_cost, new_pos, path + [new_pos], d))
        if tick < 20:
            print(len(Q))
    return float("inf"), []  # destination is unreachable


def dijkstra(board, start, end, least, most):
    tick = 0
    Q = [(0, *start, 0, 0)]
    visited = set()
    while Q:
        tick += 1
        cost, x, y, px, py = heapq.heappop(Q)
        if (x, y) == end:
            return cost
        if (x, y, px, py) in visited:
            continue
        visited.add((x, y, px, py))
        # calculate turns only
        dirs = {(1, 0), (0, 1), (-1, 0), (0, -1)} - {(px, py), (-px, -py)}
        for dx, dy in dirs:
            a, b, new_cost = x, y, cost
            # enter 4-10 moves in the chosen direction
            for i in range(1, most + 1):
                a, b = a + dx, b + dy
                if (a, b) in board:
                    new_cost += board[a, b]
                    if i >= least:
                        heapq.heappush(Q, (new_cost, a, b, dx, dy))
        if tick < 20:
            print(len(Q))


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


def part1(input):
    h, w = len(input), len(input[0])
    M = input
    board = {(i, j): int(cell) for i, row in enumerate(input) for j, cell in enumerate(row)}

    # best_cost = search(M, (0, 0), (h - 1, w - 1))
    best_cost, path = dijkstra3(board, M, (0, 0), (h - 1, w - 1))
    print(f"Part 1: {best_cost}")

    # pt1
    print(dijkstra(board, (0, 0), max(board), 1, 3))  # board, start, end, least, most
    # pt2
    # print(dijkstra(board, (0, 0), max(board), 4, 10))

    # print_map(M, path)
    pass


def part2(input):
    print(f"Part 2: {None}")
    pass


if __name__ == "__main__":
    input = open(f"day{day}/input_{year}_{day}.txt", "r").read()
    input = [[int(ch) for ch in row] for row in input.splitlines()]
    part1(input)
    part2(input)
