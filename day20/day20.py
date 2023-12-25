import operator
import os
import re
import sys
import time
from collections import defaultdict
from copy import deepcopy
from functools import cache, lru_cache, reduce


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


class Message:
    def __init__(self, _from: str, _to: str, signal: str) -> None:
        self.signal = signal
        self._from = _from
        self._to = _to

    def __str__(self) -> str:
        return f"{self.signal} to {self._to} (src {self._from})"

    def __repr__(self) -> str:
        return self.__str__()


class Component:
    def __init__(self, label: str, type: str, connected_to=None) -> None:
        self.label = label
        self.type = type
        self.connected_to = connected_to if connected_to is not None else []
        self.output = "L"
        self.ff_memory = "L"
        self.nand_memory = {}

    def flipflop(self, msg: Message):
        prev_output = self.output
        # if len(self.connected_to) > 1:
        #    raise Exception("Not a flipflop")
        if msg.signal == "L":
            self.ff_memory = "H" if self.ff_memory == "L" else "L"
            MQ.send(self.label, self.connected_to, self.ff_memory)
        elif msg.signal == "H":
            pass  # H preserves output; no signals are sent
        else:
            raise Exception(f"Invalid signal {msg.signal}")

        self.output = self.ff_memory
        print(f"(component) flipflop {self.label} changed from {prev_output} to {self.output}")

    def nand(self, msg: Message):
        prev_output = self.output
        self.nand_memory[msg._from] = msg.signal
        inputs_in_H = [m == "H" for m in self.nand_memory.values()]
        if all(inputs_in_H) and len(inputs_in_H) == connected_outputs[self.label]:
            self.output = "L"  # all inputs == high -> output = low
        else:
            self.output = "H"  # some input == low -> output = high
        # if prev_output != self.output:
        MQ.send(self.label, self.connected_to, self.output)
        print(f"(component) nand {self.label} changed from {prev_output} to {self.output}")

    def wire(self):
        # MQ.send(self.label, self.connected_to, self.output)
        self.output = "L"
        print(f"(component) wire {self.label} sent pulse L")

    def process_signal(self, msg: Message):
        if self.type == "%":
            self.flipflop(msg)
        elif self.type == "&":
            self.nand(msg)
        else:
            self.wire(msg)

    def __str__(self) -> str:
        return f"C({self.label}) ({'FF' if self.type=='%' else ('NAND' if self.type=='&' else 'wire')}) -> {self.connected_to} == {self.output}"

    def __repr__(self) -> str:
        return self.__str__()


class MessageQueue:
    def __init__(self) -> None:
        self.queue = []
        self.pulse_cnt_low = 0
        self.pulse_cnt_high = 0
        self.is_part2 = False

    def reset_cnt(self):
        self.pulse_cnt_low = 0
        self.pulse_cnt_high = 0

    def inc_low_cnt(self):
        self.pulse_cnt_low += 1

    def send(self, src: str, dest: list, signal: str) -> None:
        for c in dest:
            msg = Message(src, c, signal)
            self.queue.append(msg)
            print(f"(add to queue) send {signal} to {c} (src = {src})")
            if signal == "L":
                self.pulse_cnt_low += 1
            else:
                self.pulse_cnt_high += 1

    def dispatch(self) -> None:
        while len(self.queue) > 0:
            message = self.queue.pop(0)
            print(f"(dispatch) {message.signal} from {message._from} to {message._to}")
            if self.is_part2 and message._to == "rx" and message.signal == "L":
                print(f"(found) Message to {message._to} dropped; component does not exist")
                raise Exception("Found rx")
            elif message._to not in C:
                print(f"(not found) Message to {message._to} dropped; component does not exist")
            else:
                dest = C[message._to]
                dest.process_signal(message)  # sends the signal to destination

    def monitor(self, pin):
        print(f"Monitoring pin {pin}...")
        while True:
            print(f"Output {pin} = {C[pin].output}")
            time.sleep(1)


def press_button(n, is_part2=False):
    cnt = 0
    print(f"--- Starting cycle of {n} button presses...")
    MQ.is_part2 = is_part2

    for i in range(n):
        # MQ.reset_cnt()
        dest = "broadcaster"
        MQ.inc_low_cnt()  # button press
        MQ.send(dest, C[dest].connected_to, "L")
        MQ.dispatch()

        print(
            f"-- Button press #{i+1} -- dispatched {MQ.pulse_cnt_low} low pulses and {MQ.pulse_cnt_high} high pulses"
        )
        print(f"-- Output {[str(C[c].label) + '=' + str(C[c].output) for c in C]}")
        print("\n\n\n")
        if False and is_part2:
            print(f"Part 2: {i+1} button presses to get output of rx to pulse low")
            cnt = i
            break
    return (MQ.pulse_cnt_low, MQ.pulse_cnt_high) if is_part2 == False else cnt + 1


def part1():
    low_cnt, high_cnt = press_button(1000)
    print(f"Part 1: {low_cnt} low pulses + {high_cnt} high pulses = {low_cnt*high_cnt}")


def part2():
    press_button(100000, is_part2=True)
    print(f"Part 2: {None}")
    pass


if __name__ == "__main__":
    LOW = "L"
    HIGH = "H"
    input = [line for line in input.splitlines()]
    C = {}  # components
    MQ = MessageQueue()  # queue
    connected_outputs = defaultdict(int)

    for line in input:
        label, rest = line.split(" -> ")
        component_type = label[0]
        connected_to = rest.split(", ")
        label = label[1:] if component_type in ["%", "&"] else label
        C[label] = Component(label, component_type, connected_to)
        for c in connected_to:
            connected_outputs[c] += 1

    # part1()
    part2()


# broadcaster -> a, b, c
# %a -> b
# %b -> c
# %c -> inv
# &inv -> a
