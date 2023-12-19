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
    print(f"Processing rule {wfname}")
    for conditions in W[wfname]["conditions"]:
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
        return W[wfname]["outcomes"]


def process_part(part):
    next_wflow = "in"
    value = 0
    while True:
        outcome = workflow(part, next_wflow)
        print(f"Processing part {part}, outcome: {outcome}")
        if outcome == "R":
            return 0
        elif outcome == "A":
            value = sum([int(c.split("=")[1]) for c in part.split(",")])
            print(f"accepted part {part}, amount {value}")
            return value
        else:
            next_wflow = outcome


def part1(input):
    total_accepeted = 0
    for p_no, part in P.items():
        total_accepeted += process_part(part)

    print(f"Part 1: {total_accepeted}")
    pass


def part2(input):
    # px{a<2006:qkq,m>2090:A,rfg}
    # pv{a>1716:R,A}
    # lnx{m>1548:A,A}
    # rfg{s<537:gd,x>2440:R,A}
    # qs{s>3448:A,lnx}
    # qkq{x<1416:A,crn}
    # crn{x>2662:A,R}
    # in{s<1351:px,qqz}
    # qqz{s>2770:qs,m<1801:hdj,R}
    # gd{a>3333:R,R}
    # hdj{m>838:A,pv}
    Q = []
    combinations = 0
    for wfname, workflow in W.items():
        for condition in workflow["conditions"]:
            c, next_step = condition.split(":")
            if next_step != "A":
                continue
            delta = 0
            if ">" in c:
                val = int(c.split(">")[1])
                delta = 4000 - val
            elif "<" in c:
                val = int(c.split("<")[1])
                delta = val
            else:
                print("Error")
                sys.exit(0)
            combinations += 3999 * 3999 * 3999 * delta
            # pairs = parts.split(",")
            # parts_val = {key: int(value) for key, value in (pair.split("=") for pair in pairs)}
            # result = eval(c, parts_val)
        print(f"Wworkflow {wfname}, workflow {workflow}, combinations {combinations}")
    print(f"Part 2: {combinations}")
    print(f"Part 2: {None}")
    pass


# 167409079868000
# 692600289949170
# 693120000000000

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
        outcomes = rules[-1]
        rules = rules[:-1]
        # assert len(rules) == 1
        W[workflow_name] = {"conditions": rules, "outcomes": outcomes}
        i += 1
        r += 1

    # Read parts
    P, p = {}, 0
    i += 1
    while i < len(input):
        line = input[i]
        # x=787,m=2655,a=1222,s=2876
        # for ch in ["x=", "m=", "a=", "s="]:
        #    line = line.replace(ch, "")
        # x, m, a, s = line.strip("{}").split(",")
        # P[p] = {"x": x, "m": m, "a": a, "s": s}
        P[p] = line.strip("{}")
        p += 1
        i += 1

    # part1(input)
    part2(input)
