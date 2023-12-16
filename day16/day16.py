import os
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


input = open(f"day{day}/input_{year}_{day}.txt", "r").read()
input = [line for line in input.splitlines()]
M = [[ch for ch in row] for row in input]
h = len(M)
w = len(M[0])

energized = set()
reflected_beams = []


def reflect_beam(pos, dir):
    # avoid infinite loops
    if (pos, dir) in reflected_beams:
        return
    else:
        reflected_beams.append((pos, dir))

    while True:
        r, c = pos

        # beam out of bounds
        if r < 0 or r >= h or c < 0 or c >= w:
            break

        ch = M[r][c]
        energized.add((r, c))
        if ch == ".":
            pass
        elif ch == "/":
            if dir == "E":
                dir = "N"
            elif dir == "W":
                dir = "S"
            elif dir == "N":
                dir = "E"
            elif dir == "S":
                dir = "W"
        elif ch == "\\":
            if dir == "E":
                dir = "S"
            elif dir == "W":
                dir = "N"
            elif dir == "N":
                dir = "W"
            elif dir == "S":
                dir = "E"
        elif (ch == "-" and dir in ["E", "W"]) or (M[r][c] == "|" and dir in ["N", "S"]):
            pass
        elif (ch == "-" and dir in ["S", "N"]) or (M[r][c] == "|" and dir in ["E", "W"]):
            # split beams
            new_dirs = split_beam_dir(dir)
            reflect_beam(pos, new_dirs[0])
            reflect_beam(pos, new_dirs[1])
            break

        pos, dir = move_beam(pos, dir)


def split_beam_dir(dir):
    if dir in ["E", "W"]:
        return ["N", "S"]
    elif dir in ["N", "S"]:
        return ["E", "W"]
    else:
        raise ValueError(f"Invalid direction: {dir}")


def move_beam(pos, dir):
    GPS = {"E": (0, 1), "W": (0, -1), "N": (-1, 0), "S": (1, 0)}
    new_pos = (pos[0] + GPS[dir][0], pos[1] + GPS[dir][1])
    return new_pos, dir


def print_map(M):
    for r in range(len(M)):
        for c in range(len(M[0])):
            if (r, c) in energized and M[r][c] == ".":
                ch = "#"
            else:
                ch = M[r][c]
            print(ch, end="")
        print("")


def part1(input):
    pos = (0, 0)
    dir = "E"
    reflect_beam(pos, dir)
    print_map(M)
    print(f"Part 1: {len(energized)}\n\n")


def part2(input):
    global energized, reflected_beams

    # test all possible starting points
    max_energized = 0
    best_pos = None

    # top and bottom row
    for r in [0, h - 1]:
        for c in range(w):
            energized = set()
            reflected_beams = []
            reflect_beam((r, c), "S")
            if len(energized) > max_energized:
                print("new max", len(energized))
                max_energized = len(energized)
                best_pos = (r, c)

    # left and right column
    for c in [0, w - 1]:
        for r in range(h):
            energized = set()
            reflected_beams = []
            reflect_beam((r, c), "S")
            if len(energized) > max_energized:
                print("new max", len(energized))
                max_energized = len(energized)
                best_pos = (r, c)

    print(f"Part 2: best pos {best_pos} with {max_energized}")


if __name__ == "__main__":
    part1(input)
    part2(input)
