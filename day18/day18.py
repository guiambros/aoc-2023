import operator
import re
import sys
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


def shoelace_area(points):
    n = len(points)
    res = 0
    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]
        res += x1 * y2 - x2 * y1
    return abs(res // 2)


def part1(input):
    pos, path = (0, 0), [(0, 0)]
    for d, l, _ in input:
        for __ in range(l):
            pos = tuple(map(operator.add, pos, GPS[d]))
            path.append((pos))

    # print_map(path)
    print(f"Part 1: {shoelace_area(path) + len(path) // 2 + 1}")


@timer
def part2(input):
    C = {0: "R", 1: "D", 2: "L", 3: "U"}
    pos, vertices = (0, 0), [(0, 0)]
    steps = 0
    for _, _, r in input:
        direction = C[int(r[-1])]
        dist = int(r[:-1], 16)
        pos = tuple(map(operator.add, pos, map(operator.mul, GPS[direction], [dist, dist])))
        steps += dist
        vertices.append((pos))
    print(f"Part 2: {shoelace_area(vertices) + steps // 2 + 1}")


def print_map(path):
    min_y = min(path, key=lambda p: p[0])[0]
    max_y = max(path, key=lambda p: p[0])[0]
    min_x = min(path, key=lambda p: p[1])[1]
    max_x = max(path, key=lambda p: p[1])[1]
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (y, x) in path:
                print("#", end="")
            else:
                print(".", end="")
        print()


if __name__ == "__main__":
    # python array coords: (y, x)
    GPS = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}

    input = [l for l in input.splitlines()]
    input = [(r[0], int(r[1]), r[2][2:-1]) for r in (r.split(" ") for r in input)]
    part1(input)
    part2(input)
