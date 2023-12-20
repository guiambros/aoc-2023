import operator
import os
import re
import sys
import time
from collections import defaultdict
from copy import deepcopy
from functools import cache, lru_cache, reduce
from typing import Any


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


def workflow(parts, wfname):
    # print(f"Processing rule {wfname}")
    for conditions in W[wfname]["rules"]:
        for condition in conditions.split(","):
            c, next_step = condition.split(":")
            pairs = parts.split(",")
            parts_val = {key: int(value) for key, value in (pair.split("=") for pair in pairs)}

            result = eval(c, parts_val)
            if result:
                return next_step
            else:
                continue

    else:
        return W[wfname]["fallback"]


def process_part(part):
    next_wflow = "in"
    value = 0
    while True:
        outcome = workflow(part, next_wflow)
        # print(f"Processing part {part}, outcome: {outcome}")
        if outcome == "R":
            return 0
        elif outcome == "A":
            value = sum([int(c.split("=")[1]) for c in part.split(",")])
            return value
        else:
            next_wflow = outcome


def process_workflow_pt2():
    accepted_ranges = []
    rg = {key: (1, 4000) for key in "xmas"}
    Q = [("in", rg)]
    while Q:
        wf, rg = Q.pop(0)
        # print(f"Processing rule {wf}, current constraints {rg}")

        for rule in W[wf]["rules"]:
            c, next_step = rule.split(":")

            if next_step == "":  # we're done with this workflow
                accepted_ranges.append(rg)
                break

            # sample: wfname{a>1716:R,A}
            v, op, val = re.search("([x|m|a|s])\s*([<>=]+)\s*(\d+)", c).groups()
            T = dict(rg)
            F = dict(rg)
            if op == ">":
                T[v] = (max(rg[v][0], int(val) + 1), rg[v][1])
                F[v] = (rg[v][0], min(rg[v][1], int(val)))
            elif op == "<":
                T[v] = (rg[v][0], min(rg[v][1], int(val) - 1))
                F[v] = (max(rg[v][0], int(val)), rg[v][1])

            # possible outcomes: A, R, or next workflow
            if next_step == "R":
                pass
            elif next_step == "A":
                accepted_ranges.append(T)
            else:
                Q.append((next_step, T))

            rg = F  # continue processing the flow with the remaining non-true elements

        # process the fallback
        fallback = W[wf]["fallback"]
        if fallback == "R":
            pass
        elif fallback == "A":
            accepted_ranges.append(rg)
        else:
            Q.append((fallback, rg))
        pass

    # count range span
    total = 0
    for rg in accepted_ranges:
        deltas = [max(0, rg[key][1] - rg[key][0] + 1) for key in "xmas"]
        total += reduce(operator.mul, deltas, 1)
    return total


def part1(input):
    total_accepeted = 0
    for p_no, part in P.items():
        total_accepeted += process_part(part)

    print(f"Part 1: {total_accepeted}")
    pass


def part2(input):
    Q = []
    combinations = 0
    result = process_workflow_pt2()
    print(f"Part 2: {result}")


if __name__ == "__main__":
    # -- input in multiple lines
    input = [line for line in input.splitlines()]

    # Read workflows
    i, r = 0, 0
    W = {}
    while True:
        line = input[i]
        if line == "":
            break
        workflow_name, rules = line.split("{")
        rules = rules.strip("}").split(",")
        fallback = rules[-1]
        rules = rules[:-1]
        W[workflow_name] = {"rules": rules, "fallback": fallback}
        i += 1
        r += 1

    # Read parts
    P, p = {}, 0
    i += 1
    while i < len(input):
        line = input[i]
        P[p] = line.strip("{}")
        p += 1
        i += 1

    part1(input)
    part2(input)
