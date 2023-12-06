import functools
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


input = open(f"day{day}/input_{year}_{day}.txt", "r").read().splitlines()


@functools.lru_cache(maxsize=None)  # maxsize=None for unlimited cache size
def pow_2(n):
    return 2**n


class Card:
    def __init__(self, id, win_num, my_num):
        self.id = int(id)
        self.win_num = win_num
        self.my_num = my_num
        self.remaining = 1


def decode_cards(input):
    cards = {}
    for l in input:
        card_num, numbers = l.split(":")
        id = card_num.split(" ")[-1]
        winning_numbers, my_numbers = numbers.split("|")
        winning_numbers = [int(n) for n in winning_numbers.strip().split(" ") if len(n) > 0]
        my_numbers = [int(n) for n in my_numbers.strip().split(" ") if len(n) > 0]
        cards[id] = Card(id, winning_numbers, my_numbers)
    return cards


def part1(input):
    score = 0
    for id, card in cards.items():
        matches = len(set(card.win_num) & set(card.my_num))
        if matches > 0:
            score += pow_2(matches - 1)

    print(f"Part 1: final score {score}")
    pass


def part2(input):
    total_cards = len(cards)
    i = 0
    for n in range(1, len(cards) + 1):
        i += 1
        if i % 10 == 0:
            print("processing card", n)
        card = cards[str(n)]
        while card.remaining > 0:
            card.remaining -= 1
            matches = len(set(card.win_num) & set(card.my_num))

            # copy the next n matches to the cards_queue
            for n_copy in range(matches):
                cards[str(int(card.id) + n_copy + 1)].remaining += 1
                total_cards += 1

    print(f"Part 2: total num of cards {total_cards}")


if __name__ == "__main__":
    cards = decode_cards(input)
    part1(input)
    part2(input)
