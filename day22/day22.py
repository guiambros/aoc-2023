import operator
import os
import re
import sys
import time
from collections import defaultdict
from copy import deepcopy
from functools import cache, lru_cache, reduce
from typing import Any, List, Tuple


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


class Brick:
    def __init__(self, start: tuple, end: tuple, id=None) -> None:
        self.x1 = start[0]
        self.y1 = start[1]
        self.z1 = start[2]
        self.x2 = end[0]
        self.y2 = end[1]
        self.z2 = end[2]
        self.id = id
        pass

    def intersects(self, other, delta_z: int = 0) -> bool:
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
            and self.z1 <= other.z2 + delta_z
            and self.z2 >= other.z1 + delta_z
        )

    def key_z(self) -> int:
        return max(self.z1, self.z2)

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"Brick {self.id}: ({self.x1},{self.y1},{self.z1}) ~ ({self.x2},{self.y2},{self.z2})"


class Map:
    def __init__(self, B: list) -> None:
        self.bricks = B

    def move(self, b: Brick, new_z: int) -> None:
        if conflict := self.find_bricks_pos(b.x1, b.y1, b.z1, b.id):
            print(f"Brick {b.id} can not be moved to {new_z} -- conflicts with {conflict}")
            raise Exception("Brick can not be moved")
        delta = new_z - b.z1
        b.z1 += delta
        b.z2 += delta
        return

    def lower_settled_bricks(self, id) -> list:
        return [b for b in self.bricks[:id]]

    def upper_bricks(self, id) -> list:
        return [b for b in self.bricks[id + 1 :]]

    def find_bricks_above(self, b: Brick) -> list:
        return [
            o
            for o in self.upper_bricks(b.id)
            if b.z1 <= (o.z1 - 1) <= b.z2 and o.intersects(b, delta_z=1)
        ]

    def find_bricks_below(self, b: Brick) -> list:
        return [o for o in self.lower_settled_bricks(b.id) if o.intersects(b, delta_z=-1)]

    def find_bricks_pos(self, x: int, y: int, z: int, id: int) -> list:
        found = [
            o for o in self.bricks if o.x1 <= x <= o.x2 and o.y1 == y <= o.y2 and o.z1 <= z <= o.z2
        ]
        return [f for f in found if f.id != id]


@timer
def part1(M: list) -> list:
    # make bricks fall
    zmax_highest_settled_brick = B[0].z2
    for _, b in enumerate(M.bricks):
        if _ % 100 == 0:
            print(f"Processing brick {_} of {map_size}")

        mod_flag = True
        while mod_flag:
            mod_flag = False

            # if brick is already on the min_z floor, stop
            if b.z1 == 1:
                break

            # if we're far from the current floor, fast track them down
            if b.z1 > zmax_highest_settled_brick:
                M.move(b, zmax_highest_settled_brick + 1)

            # now move this brick carefully down, avoiding overlapping other bricks
            while min(b.z1, b.z2) > 1 and not M.find_bricks_below(b):
                M.move(b, b.z1 - 1)
                mod_flag = True
            zmax_highest_settled_brick = max(b.z2, zmax_highest_settled_brick)

    # check which bricks can be removed without collapsing the structure
    can_be_removed = []
    for b in M.bricks:
        U = M.find_bricks_above(b)
        cbr = all([len(M.find_bricks_below(u)) > 1 for u in U])
        if cbr:
            can_be_removed.append(b)
            print(f"Brick {b.id} can be safely removed")

    print(f"Part 1: {len(can_be_removed)}")
    return can_be_removed


def part2(input):
    # Part 2 is too painful; decided to skip it.

    print(f"Part 2: {None}")
    pass


if __name__ == "__main__":
    map_size = len(input.splitlines())
    B = []
    for id, line in enumerate(input.splitlines()):
        b_start = tuple([int(i) for i in line.split("~")[0].split(",")])
        b_end = tuple([int(i) for i in line.split("~")[1].split(",")])
        B.append(Brick(b_start, b_end, id))
    B.sort(key=lambda z: z.key_z())
    # reorder IDs
    for i, b in enumerate(B):
        b.id = i
    M = Map(B)
    part1(M)  # 401
    part2(M)  # 63491
