import operator
import os
import re
import sys
from collections import Counter, defaultdict
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
input = [line for line in input.splitlines()]

Deck = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}


def score(hand):
    ranking = 0
    s = Counter(hand)
    eq = s.most_common()[0][1]

    if eq == 5:  # royal flush
        ranking += 6
    elif eq == 4:  # four of a kind
        ranking += 5
    elif eq == 3 and len(s) == 2:  # full house
        ranking += 4
    elif eq == 3:  # three of a kind
        ranking += 3
    elif eq == 2 and len(s) == 3:  # two pairs
        ranking += 2
    elif eq == 2:  # one pair
        ranking += 1
    else:
        ranking += 0  # high card
    return ranking


def index_hand(hand, bet):
    if "J" in hand:
        s = max(score(hand.replace("J", ch)) for ch in Deck)  # brute force
    else:
        s = score(hand)
    indiv_scores = tuple([Deck[ch] for ch in hand])
    return tuple([s]) + (indiv_scores) + tuple([hand]) + tuple([int(bet)])


def part1(input):
    hands = []
    for l in input:
        hand, bet = l.split(" ")
        hands.append(index_hand(hand, bet))

    hands = sorted(hands)
    total_winnings = sum([s[-1] * (rank + 1) for rank, s in enumerate(hands)])

    print(f"Part 1: {total_winnings}")


def part2(input):
    Deck["J"] = 1
    hands = []
    for l in input:
        hand, bet = l.split(" ")
        hands.append(index_hand(hand, bet))

    hands = sorted(hands)
    total_winnings = sum([s[-1] * (rank + 1) for rank, s in enumerate(hands)])

    print(f"Part 2: {total_winnings}")


if __name__ == "__main__":
    part1(input)
    part2(input)
