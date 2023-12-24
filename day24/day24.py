import operator
import os
import random
import re
import statistics
import sys
import time
from collections import defaultdict
from copy import deepcopy
from functools import cache, lru_cache, reduce
from itertools import combinations

import numpy as np
import sympy as sp
from scipy.optimize import fsolve


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


def calc_line_params(eq):
    (px, py, _), (vx, vy, _) = eq
    return (vy / vx), (py - px * (vy / vx))


def part1():
    def intersected_in_past(h1, h2, intersection):
        (px1, py1, pz1), (vx1, vy1, vz1) = h1
        (px2, py2, pz2), (vx2, vy2, vz2) = h2
        intersection_x, intersection_y, intersection_z = intersection

        if vx1 == 0 and vx2 == 0:
            return not (px1 == px2 and py1 == py2)

        if vx1 == 0:
            return intersection_x == px1 and intersection_y == py2

        if vx2 == 0:
            return intersection_x == px2 and intersection_y == py1

        t1 = (intersection_x - px1) / vx1
        t2 = (intersection_x - px2) / vx2
        return t1 < 0 or t2 < 0

    lower_boundary, upper_boundary = 7, 27
    lower_boundary, upper_boundary = 200000000000000, 400000000000000
    cnt = 0
    for i, pair in enumerate(combinations(H, 2)):
        h1, h2 = pair
        slope1, intercept1 = calc_line_params(h1)
        slope2, intercept2 = calc_line_params(h2)
        intersection_x = (intercept2 - intercept1) / ((slope1 - slope2) + 1e-10)
        intersection_y = slope1 * intersection_x + intercept1
        valid_pair = False
        if (
            intersection_x >= lower_boundary
            and intersection_x <= upper_boundary
            and intersection_y >= lower_boundary
            and intersection_y <= upper_boundary
        ) and not intersected_in_past(h1, h2, (intersection_x, intersection_y, 0)):
            valid_pair = True
            cnt += 1

        print(f"For pair {i} -- intersection at {intersection_x}, {intersection_y} -- {valid_pair}")
    return cnt


# Define the system of equations
def equations(vars, object_positions, object_velocities):
    P0x, P0y, P0z, V0x, V0y, V0z, t1, t2, t3 = vars

    # Equations for each object at interception time
    eqs = []
    for i in range(3):
        posx, posy, posz = object_positions[i]
        velx, vely, velz = object_velocities[i]
        t = [t1, t2, t3][i]
        eqs.append(P0x + V0x * t - (posx + velx * t))
        eqs.append(P0y + V0y * t - (posy + vely * t))
        eqs.append(P0z + V0z * t - (posz + velz * t))

    return eqs


# For part two, we need to find 6 variables: (px, py, pz), and velocity vector (vx, vy, vz).
#
# For each hailstone, we know we'll intercept at a time tA, so we add 1 unknown variable
# This means we need a total of 3 hailstone trajectories to be able to find our answer
# (9 equations, for 6 unknowns + 3 intercept times)
#
# I tried numerically first, but it doesn't converge nicely to the answer; probably
# due to numerical instability. My brute force approach was to try 1000 random combinations
# of 3 hailstones, and take the mode of the results. Not nice, but it works.
#
# I then solved symbolically using SymPy, and it worked beautifully :)
#
def part2_numerically():
    all_res = []
    for i in range(1000):
        res = sum(solve_numerically()[:3])
        print(f"Solving pt2 numerically -- #{i} -- {res}")
        all_res.append(res)
    mode = statistics.mode(all_res)
    return int(mode)


def solve_numerically():
    R = random.sample(H, 3)
    pos_x1, pos_y1, pos_z1 = R[0][0]
    vel_x1, vel_y1, vel_z1 = R[0][1]

    pos_x2, pos_y2, pos_z2 = R[1][0]
    vel_x2, vel_y2, vel_z2 = R[1][1]

    pos_x3, pos_y3, pos_z3 = R[2][0]
    vel_x3, vel_y3, vel_z3 = R[2][1]

    # Initial positions and velocities of the objects
    object_positions = [
        [pos_x1, pos_y1, pos_z1],
        [pos_x2, pos_y2, pos_z2],
        [pos_x3, pos_y3, pos_z3],
    ]
    object_velocities = [
        [vel_x1, vel_y1, vel_z1],
        [vel_x2, vel_y2, vel_z2],
        [vel_x3, vel_y3, vel_z3],
    ]

    # Initial guesses for P0x, P0y, P0z, V0x, V0y, V0z, t1, t2, t3
    initial_guesses = [
        pos_x1 / 2,
        pos_y1 / 2,
        pos_z1 / 2,
        vel_x1 / 2,
        vel_y1 / 2,
        vel_z1 / 2,
        500000000000,
        500000000000,
        500000000000,
    ]

    # Solve the system of equations
    solution = fsolve(
        equations, initial_guesses, args=(object_positions, object_velocities), xtol=1e-12
    )
    return solution


def part2_symbolically():
    R = random.sample(H, 3)

    # Define symbols
    P0x, P0y, P0z = sp.symbols("P0x P0y P0z", real=True)
    V0x, V0y, V0z = sp.symbols("V0x V0y V0z", real=True)
    t1, t2, t3 = sp.symbols("t1 t2 t3", real=True)
    times = [t1, t2, t3]
    pos_x1, pos_y1, pos_z1 = R[0][0]
    vel_x1, vel_y1, vel_z1 = R[0][1]
    pos_x2, pos_y2, pos_z2 = R[1][0]
    vel_x2, vel_y2, vel_z2 = R[1][1]
    pos_x3, pos_y3, pos_z3 = R[2][0]
    vel_x3, vel_y3, vel_z3 = R[2][1]

    pos = [(pos_x1, pos_y1, pos_z1), (pos_x2, pos_y2, pos_z2), (pos_x3, pos_y3, pos_z3)]
    vel = [(vel_x1, vel_y1, vel_z1), (vel_x2, vel_y2, vel_z2), (vel_x3, vel_y3, vel_z3)]

    # Define the system of equations
    equations = []
    for i in range(3):
        equations.append(sp.Eq(P0x + V0x * times[i], pos[i][0] + vel[i][0] * times[i]))
        equations.append(sp.Eq(P0y + V0y * times[i], pos[i][1] + vel[i][1] * times[i]))
        equations.append(sp.Eq(P0z + V0z * times[i], pos[i][2] + vel[i][2] * times[i]))

    # Solve the system of equations
    solution = sp.solve(equations, [P0x, P0y, P0z, V0x, V0y, V0z, t1, t2, t3])

    return solution[0], sum(solution[0][:3])
    assert sum(solution[0][:3]) == 600352360036779


if __name__ == "__main__":
    # -- input in multiple lines
    H = []
    input = [line for line in input.splitlines()]
    for l in input:
        pos, speed = l.split(" @ ")
        pos = [int(c) for c in pos.split(", ")]
        speed = [int(c) for c in speed.split(", ")]
        px, py, pz = pos
        vx, vy, vz = speed
        H.append(((px, py, pz), (vx, vy, vz)))

    pt1_cnt = part1()
    pt2_num = part2_numerically()
    vars, sol = part2_symbolically()

    print(f"Part 1: {pt1_cnt}")
    print(f"Part 2 (numerically): mode {pt2_num}")
    print(f"Part 2 (symbolically): {vars} == {sol}")
