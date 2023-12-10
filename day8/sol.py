import math


def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)


def lcm_of_array(numbers):
    print(numbers)
    result = numbers[0]
    for num in numbers[1:]:
        result = lcm(result, num)
    return result


with open("day8/input_2023_8.txt", "r") as file:
    instructions, directions = file.read().split("\n\n")

instructions = list(instructions)
directions_dict = {}
locations = []

directions = directions.splitlines()
for item in directions:
    current_location, next_locations = item.split(" = ")
    next_locations = tuple(next_locations.strip("()").split(", "))
    directions_dict[current_location] = next_locations
    if current_location.endswith("A"):
        locations.append(current_location)

count_array = []

for i, current_location in enumerate(locations):
    count = 0
    current_instruction_index = 0
    while not current_location.endswith("Z"):
        count += 1
        current_instruction = instructions[current_instruction_index]
        if current_instruction == "L":
            current_location = directions_dict[current_location][0]
        else:
            current_location = directions_dict[current_location][1]

        if current_instruction_index == len(instructions) - 1:
            current_instruction_index = 0
        else:
            current_instruction_index += 1
    count_array.append(count)

ans = lcm_of_array(count_array)
print(ans)
