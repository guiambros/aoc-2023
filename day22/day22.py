import operator
import os
import re
import sys
import time
from collections import defaultdict
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


# get current day from path and read input data
cwd = sys.argv[0]
if not ("day" in cwd):
    print("Run this from the day directory")
    sys.exit(0)
year = int(re.search("\\d{4}", cwd).group(0))
day = int(re.search("\\/day(\\d+)", cwd).group(1))
input = open(f"day{day}/input_{year}_{day}.txt", "r").read()


class Map:
    def __init__(self):
        self._map = defaultdict(int)

    def set(self, x, y, z, value):
        self._map[(x, y, z)] = value

    def set_range(self, c1, c2, id):
        for x in range(c1[0], c2[0] + 1):
            for y in range(c1[1], c2[1] + 1):
                for z in range(c1[2], c2[2] + 1):
                    self.set(x, y, z, id)

    def get(self, x, y, z):
        return self._map.get((x, y, z))

    def remove(self, x, y, z):
        del self._map[(x, y, z)]

    def contains(self, x, y, z):
        return (x, y, z) in self._map

    def get_brick_coords(self, id):
        coords = []
        for k, v in self._map.items():
            if v == id:
                coords.append(k)
        return coords

    def get_brick_id(self, coords):
        brick_ids = set()
        for c in coords:
            brick_ids.add(0 if c[2] == 0 else self.get(c[0], c[1], c[2]))
        brick_ids.discard(None)
        return brick_ids

    def del_brick(self, id):
        coords = self.get_brick_coords(id)
        for c in coords:
            self.remove(c[0], c[1], c[2])

    def is_empty(self, coords_array):
        for c in coords_array:
            if self.contains(c[0], c[1], c[2]):
                return False
        return True

    def cnt_bricks_below(self, id):
        coords = self.get_brick_coords(id)
        min_z = min([c[2] for c in coords])
        coords_below = list(set([(c[0], c[1], min_z - 1) for c in coords]))
        # assert None not in self.get_brick_id(coords_below)
        return len(self.get_brick_id(coords_below))

    def find_bricks_above(self, coords, my_id):
        ids = self.get_brick_id([[c[0], c[1], c[2] + 1] for c in coords])
        if ids == {my_id}:
            return self.find_bricks_above([[c[0], c[1], c[2] + 1] for c in coords], my_id)
        return ids


def part1(B):
    M = Map()
    for id, b in enumerate(B):
        M.set_range(b[0], b[1], id + 1)

    # make bricks fall
    for b in range(1, map_size + 1):
        mod_flag = True
        while mod_flag:
            mod_flag = False
            brick_coords = M.get_brick_coords(b)
            min_z = min([c[2] for c in brick_coords])
            if min_z == 1:
                break
            c_below = list(set([(c[0], c[1], min_z - 1) for c in M.get_brick_coords(b)]))
            if M.is_empty(c_below):
                M.del_brick(b)
                for c in brick_coords:
                    M.set(c[0], c[1], c[2] - 1, b)
                mod_flag = True

    # now decide which bricks can be removed
    cnt = 0
    for b in range(1, map_size + 1):
        bricks_above = M.find_bricks_above(M.get_brick_coords(b), my_id=b)
        can_be_removed = True
        for b_above in bricks_above:
            if M.cnt_bricks_below(b_above) < 2:
                can_be_removed = False
                print(f"Brick {b} can NOT be safely removed")
                break
        if can_be_removed:
            print(f"Brick {b} can be safely removed")
            cnt += 1
        pass

    print(f"Part 1: {cnt}")
    pass


def part2(input):
    print(f"Part 2: {None}")
    pass


if __name__ == "__main__":
    map_size = len(input.splitlines())

    # -- input in multiple lines
    b_start = [
        tuple([int(i) for i in line.split("~")[0].split(",")]) for line in input.splitlines()
    ]
    b_end = [tuple([int(i) for i in line.split("~")[1].split(",")]) for line in input.splitlines()]

    B = [(bs, be) for bs, be in zip(b_start, b_end)]
    part1(B)  # 401
    part2(B)  # 63491
