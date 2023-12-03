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


def get_number(input, row, col):
    number = []
    coords = []

    # find the starting position of the number
    while col >= 1 and input[row][col - 1].isdigit():
        col -= 1

    # get the full number
    while col < len(input[row]) and input[row][col].isdigit():
        number.append(input[row][col])
        coords.append((row, col))
        col += 1

    return int("".join(number)), coords


# check if there's a symbol somewhere close to this digit
def check_if_valid_number(input, row, col, is_part2=False):
    coords = [
        (row - 1, col - 1),
        (row - 1, col),
        (row - 1, col + 1),
        (row, col - 1),
        (row, col + 1),
        (row + 1, col - 1),
        (row + 1, col),
        (row + 1, col + 1),
    ]
    for r, c in coords:
        if r >= 0 and r < len(input) and c >= 0 and c < len(input[r]):
            ch = input[r][c]
            if not is_part2 and not ch.isdigit() and ch != ".":
                return True
            elif is_part2 and ch == "*":
                return True
    return False


def find_nearby_numbers(input, row, col):
    numbers = []
    coords_processed = []
    delta_coords = [
        (row - 1, col - 1),
        (row - 1, col),
        (row - 1, col + 1),
        (row, col - 1),
        (row, col + 1),
        (row + 1, col - 1),
        (row + 1, col),
        (row + 1, col + 1),
    ]
    for r, c in delta_coords:
        if (
            0 <= r < len(input)
            and 0 <= c < len(input[r])
            and (r, c) not in coords_processed
            and input[r][c].isdigit()
        ):
            ch = input[r][c]
            if ch.isdigit() and (r, c) not in coords_processed:
                num, coords = get_number(input, r, c)
                coords_processed += coords
                numbers.append(num)

    return numbers


def part1(input):
    numbers = []
    for row, l in enumerate(input):
        decoding_number = False
        valid_number = False
        number = None
        for col, ch in enumerate(l):
            if ch.isdigit():
                if not decoding_number:  # get the full number on the first digit found
                    number, _ = get_number(input, row, col)
                    decoding_number = True

                if not valid_number:  # check if there's a symbol somewhere close to this digit
                    if check_if_valid_number(input, row, col):
                        numbers.append(number)
                        valid_number = True
            else:
                decoding_number = False
                valid_number = False
                number = None
    print(f"Part 1: total sum of valid numbers {sum(numbers)}")


def part2(input):
    numbers = []
    gears = []
    for row, l in enumerate(input):
        for col, ch in enumerate(l):
            if ch == "*":
                numbers = find_nearby_numbers(input, row, col)
                if len(numbers) == 2:
                    gears.append(numbers[0] * numbers[1])
    print(f"Part 2: total sum of gears multiplied {sum(gears)}")


if __name__ == "__main__":
    part1(input)
    part2(input)
