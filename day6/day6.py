import operator
import sys
from functools import reduce

# get current day
cwd = sys.argv[0]
if not ("day" in cwd):
    print("Run this from the day directory")
    sys.exit(0)

times = [59, 68, 82, 74]
distances = [543, 1020, 1664, 1022]


def part1(input):
    ways_to_wins = []
    for t, d_max in zip(times, distances):
        wins = 0
        for t_wait in range(t):
            dist = (t - t_wait) * t_wait
            if dist > d_max:
                wins += 1
        ways_to_wins.append(wins)
    print(f"Part 1: ways to win {ways_to_wins} == {reduce(operator.mul, ways_to_wins)}")


def part2(input):
    t = 59688274
    d_max = 543102016641022
    # t, d_max = 71530, 940200

    # find the time that we start winning
    low, high = None, None
    for t_wait in range(t):
        dist = (t - t_wait) * t_wait
        if dist > d_max:
            low = t_wait
            print("found point we start winning (low bound)== ", t_wait)
            break

    # find the time that we stop winning
    for t_wait in range(t, 0, -1):
        dist = (t - t_wait) * t_wait
        if dist <= d_max:
            continue
        else:
            high = t_wait
            print("found point we start losing (high bound) == ", t_wait)
            break

    print(f"Part 2: {high-low+1}")


if __name__ == "__main__":
    part1(input)
    part2(input)
