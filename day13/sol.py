import sys


def read_patterns():
    input = open(f"day13/input_2023_13.txt", "r").read()
    pats = [[row for row in grid.split("\n") if row] for grid in input.split("\n\n")]
    return pats


def transpose(pat):
    return ["".join([row[j] for row in pat]) for j in range(len(pat[0]))]


def dist(s1, s2):
    return sum([0 if c1 == c2 else 1 for (c1, c2) in zip(s1, s2)])


def horizontal_value(pat, needed_dist=1):
    res = 0
    for i in range(len(pat) - 1):
        tot_dist = 0
        for row1, row2 in zip(pat[i + 1 :], pat[i::-1]):
            tot_dist += dist(row1, row2)
        if tot_dist == needed_dist:
            res += i + 1
    print(f"Found horizontal mirror {res}")
    return res


def get_value(pat, needed_dist=1):
    # return horizontal_value(pat, needed_dist) * 100 + horizontal_value(transpose(pat), needed_dist)
    # return horizontal_value(transpose(pat), needed_dist)
    return horizontal_value(pat, needed_dist) * 100 + horizontal_value(transpose(pat), needed_dist)
    # return (
    #    horizontal_value(pat, needed_dist) * 100
    # )  # + horizontal_value(transpose(pat), needed_dist)


if __name__ == "__main__":
    pats = read_patterns()

    part2 = False
    print(sum([get_value(pat, 1 if part2 else 0) for pat in pats]))
