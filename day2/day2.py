import operator
import os
import re
import sys
from collections import defaultdict
from copy import deepcopy
from functools import reduce

# get current day
cwd = sys.argv[0]
if not ("day" in cwd):
    print("Run this from the day directory")
    sys.exit(0)

# read input data
year = int(re.search("\\d{4}", cwd).group(0))
day = int(re.search("\\/day(\\d+)", cwd).group(1))
input = open(f"day{day}/input_{year}_{day}.txt", "r").read()

# pattern = r"(Game \d+): ((\d+ (blue|red|green)[,;] )+)"

# input = open(f"day{day}/input_{year}_{day}_test.txt", "r").read()

# input in multiple lines
input = [line for line in input.splitlines()]

# input in a single line
# input = [line for line in input.split(",")]

# convert list to int
# input = [int(i) for i in input]


def part1(G):
    max_r = 12
    max_g = 13
    max_b = 14
    valid_games = []
    for id, games in G.items():
        if all(g.r <= max_r and g.g <= max_g and g.b <= max_b for g in games):
            valid_games.append(int(id))
    print(f"Part 1: sum of ids of valid games {sum(valid_games)}")


def part2(G):
    power_total = 0

    for _, games in G.items():
        max_r = max_g = max_b = 0
        for g in games:
            max_r = max(max_r, g.r)
            max_g = max(max_g, g.g)
            max_b = max(max_b, g.b)
        power = max_r * max_g * max_b
        power_total += power

    print(f"Part 2: total power {power_total}")
    pass


class Game:
    def __init__(self) -> None:
        self.r = 0
        self.g = 0
        self.b = 0

    def __str__(self) -> str:
        return f"({self.r}, {self.g}, {self.b})"

    __repr__ = __str__


def decode_color(games):
    games_rgb = []
    color_map = {"red": "r", "green": "g", "blue": "b"}
    for game in games:
        g = Game()
        for color in game.split(", "):
            val, col = color.split(" ")
            setattr(g, color_map[col], int(val))
        games_rgb.append(g)
    return games_rgb


def parse_input(input):
    G = {}
    for l in input:
        l = l.split("Game ")[1]
        id = l.split(":")[0]
        games = l.split(":")[1].strip().split("; ")
        games_rgb = decode_color(games)
        G[id] = games_rgb
    return G


# Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1

if __name__ == "__main__":
    G = parse_input(input)
    part1(G)
    part2(G)

# Example of an input that requires regex parsing
# Format:
#   kvlbq (22)
#   rdrad (6) -> gwyfm, fozyip, uotzz, fmkkz
#   oqbfkud (470) -> rnbqhk, mepez, mnksdxf, mjsck, bbfaxid, nglea
#   zzjyw (91)
#
# t = dict( \
#    (m[0], (int(m[1]), m[3].split(", ") if m[3] else [])) \
#       for m in [re.match("(\w+) \((\d+)\)( -> ((\w+, )*\w+))?", l).groups() \
#       for l in d] \
# )
