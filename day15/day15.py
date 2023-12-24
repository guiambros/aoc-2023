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


def hash(seq):
    code = 0
    for ch in seq:
        code += ord(ch)
        code *= 17
        code %= 256
    return code


def hash_input(input):
    codes = []
    for seq in input:
        codes.append(hash(seq))
    return sum(codes)


def part1(input):
    hashed = hash_input(input)
    print(f"Part 1: {hashed}\n\n")


class Lens:
    def __init__(self, label, fl) -> None:
        self.focal_length = fl
        self.label = label

    def __str__(self) -> str:
        return f"Lens {self.label}, focal length {self.focal_length}"

    def __repr__(self) -> str:
        return self.__str__()


class Box:
    SIZE = 9

    def __init__(self, id) -> None:
        self.slots = [None for _ in range(self.SIZE)]
        self.id = id

    def add(self, label, fl) -> None:
        i = 0
        first_empty = self.SIZE
        label_exists = None
        while i < self.SIZE:
            if self.slots[i] is None:
                first_empty = min(first_empty, i)
            elif self.slots[i].label == label:
                label_exists = i + 1
            i += 1

        if label_exists:
            self.slots[label_exists - 1] = Lens(label, fl)
            print(
                f"  -- Replaced old lens {label}/{self.slots[label_exists-1].focal_length} for lens {label}/{fl} in box {self.id}"
            )
        else:
            self.slots[first_empty] = Lens(label, fl)
            print(f"  -- Added lens {label}/{fl} to box {self.id}")
        return

    def remove_lens(self, lens_label) -> None:
        for i in range(self.SIZE):
            if self.slots[i] and self.slots[i].label == lens_label:
                self.slots.pop(i)
                break
        self.slots.extend([None] * (self.SIZE - len(self.slots)))
        print(f"  -- Removed lens {lens_label} from box {self.id}")

    def __str__(self) -> str:
        return str(self.slots)


def focusing_power(box_no, slot, focus_length):
    return (box_no + 1) * (slot + 1) * focus_length


def score_pt2(B):
    total_score = 0
    for box in B:
        for i in range(len(box.slots)):
            if box.slots[i] is None:
                continue
            score = focusing_power(box.id, i, box.slots[i].focal_length)
            print(
                f"Box {box.id}, slot {i}, lens {box.slots[i].label}/ {box.slots[i].focal_length} = score {score}"
            )
            total_score += score
    return total_score


def part2(input):
    B = [Box(i) for i in range(256)]

    for seq in input:
        op = "-" if "-" in seq else "="
        label, lens_fl = re.split("-|=", seq)
        lens_fl = None if not lens_fl else int(lens_fl)
        # print(f"{label} {op} {lens}")

        box = hash(label)
        if op == "-":
            print(f"Removed lens_label {label} from box {box}")
            B[box].remove_lens(label)

        elif op == "=":
            print(f"Added lens_label {label} with focal lenght {lens_fl} to box {box}")
            B[box].add(label, lens_fl)

    score = score_pt2(B)
    print(f"Part 2: {score}")
    pass


if __name__ == "__main__":
    # -- input in multiple lines
    input = [line for line in input.split(",")]
    part1(input)
    part2(input)
