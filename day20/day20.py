import re
import sys
import time
from collections import defaultdict
import math
from functools import reduce
import graphviz

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
        if msg.signal == "L":
            self.ff_memory = "H" if self.ff_memory == "L" else "L"
            MQ.send(self.label, self.connected_to, self.ff_memory)
        elif msg.signal == "H":
            pass  # H preserves output; no signals are sent
        else:
            raise Exception(f"Invalid signal {msg.signal}")

        self.output = self.ff_memory
        log(f"(component) flipflop {self.label} changed from {prev_output} to {self.output}")

    def nand(self, msg: Message):
        prev_output = self.output
        self.nand_memory[msg._from] = msg.signal
        inputs_in_H = [m == "H" for m in self.nand_memory.values()]
        if all(inputs_in_H) and len(inputs_in_H) == connected_outputs[self.label]:
            self.output = "L"  # all inputs == high -> output = low
        else:
            self.output = "H"  # some input == low -> output = high
        MQ.send(self.label, self.connected_to, self.output)
        log(f"(component) nand {self.label} changed from {prev_output} to {self.output}")

    def wire(self):
        self.output = "L"
        log(f"(component) wire {self.label} sent pulse L")

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
        self.part2_cycle_len = defaultdict(list)

        # NANDs to monitor for part 2; obtained by visual inspection.
        # Option 1: use graph_components()
        # Option 2: check which component are connected to rx ("nc"), and
        #           then find NANDs connected to those components.
        # nands_to_watch = ["lk", "fn", "fh", "hh"] 
        source_to_rx = [k for k,v in C.items() if "rx" in v.connected_to][0]
        self.part2_nands_to_watch = [k for k,v in C.items() if source_to_rx in v.connected_to]

    def reset_cnt(self):
        self.pulse_cnt_low = 0
        self.pulse_cnt_high = 0

    def inc_low_cnt(self):
        self.pulse_cnt_low += 1

    def send(self, src: str, dest: list, signal: str) -> None:
        # Part 2 -- Monitor the cycle length of  key NANDs in the output pipeline
        global button_press_no
        if src in self.part2_nands_to_watch and signal=="H":
            self.part2_cycle_len[src].append(button_press_no)

        # Send the signal to all connected outputs
        for c in dest:
            msg = Message(src, c, signal)
            self.queue.append(msg)
            log(f"(add to queue) send {signal} to {c} (src = {src})")
            if signal == "L":
                self.pulse_cnt_low += 1
            else:
                self.pulse_cnt_high += 1

    def dispatch(self) -> None:
        while len(self.queue) > 0:
            message = self.queue.pop(0)
            log(f"(dispatch) {message.signal} from {message._from} to {message._to}")
            if self.is_part2 and message._to == "rx" and message.signal == "L":
                log(f"(found) Message to {message._to} dropped; component does not exist")
                raise Exception("Found rx")
            elif message._to not in C:
                log(f"(not found) Message to {message._to} dropped; component does not exist")
            else:
                dest = C[message._to]
                dest.process_signal(message)  # sends the signal to destination


def log(msg):
    if logging_enabled:
        print(msg)


def press_button(n, is_part2=False):
    global button_press_no
    global nands_to_watch

    log(f"--- Starting cycle of {n} button presses...")
    MQ.is_part2 = is_part2

    for i in range(n):
        button_press_no = i
        dest = "broadcaster"
        MQ.inc_low_cnt()
        MQ.send(dest, C[dest].connected_to, "L")
        MQ.dispatch()
        log(f"-- Button press #{i+1} -- dispatched {MQ.pulse_cnt_low} low + {MQ.pulse_cnt_high} high pulses")
        log(f"-- Output {[str(C[c].label) + '=' + str(C[c].output) for c in C]}\n\n")

        if is_part2 and i % 1000 == 0:
            msg = f"#{i:<7} "
            for c in MQ.part2_nands_to_watch:
                if len(MQ.part2_cycle_len[c]) > 1:
                    msg += f" {c} @ {MQ.part2_cycle_len[c][-1] - MQ.part2_cycle_len[c][-2]}"
            log(msg)
    return (MQ.pulse_cnt_low, MQ.pulse_cnt_high) if is_part2 == False else MQ.part2_cycle_len

def lcm(numbers):
    def lcm2(a,b):
        return abs(a*b) // math.gcd(a, b)
    return reduce(lcm2, numbers, 1)

def part1():
    low_cnt, high_cnt = press_button(1000)
    print(f"Part 1: {low_cnt} low pulses + {high_cnt} high pulses = {low_cnt*high_cnt}")

def part2():
    cycle_len = press_button(15000, is_part2=True)
    cycles = [series[-1] - series[-2] for _, series in cycle_len.items()]
    print(f"Part 2: Cycles {cycles}, lcm = {lcm(cycles)}")


def graph_components():
    dot = graphviz.Digraph()

    # Add nodes
    for label, component in C.items():
        if component.type == "%":
            dot.node(
                label,
                shape="square",
                fillcolor="lightblue",
                style="filled",
                fontsize="20",
                fontname="bold",
            )
        elif component.type == "&":
            dot.node(
                label,
                shape="star",
                fillcolor="lightyellow",
                style="filled",
                fontsize="20",
                fontname="bold",
            )
        else:
            dot.node(
                label,
                shape="oval",
                fillcolor="pink",
                style="filled",
                fontsize="20",
                fontname="bold",
            )

    # Add edges
    for label, component in C.items():
        for connected_to in component.connected_to:
            dot.edge(label, connected_to)

    # Render the graph to a file (e.g., components.gv.pdf)
    dot.render("components.gv", view=True)


if __name__ == "__main__":
    LOW, HIGH = "L", "H"
    input = [line for line in input.splitlines()]
    logging_enabled = False
    C, nands, connected_outputs = {}, [], defaultdict(int)  # components

    for line in input:
        label, rest = line.split(" -> ")
        component_type = label[0]
        connected_to = rest.split(", ")
        label = label[1:] if component_type in ["%", "&"] else label
        C[label] = Component(label, component_type, connected_to)
        for c in connected_to:
            connected_outputs[c] += 1
        if component_type == "&":
            nands.append(label)

    button_press_no = 0 # used in part 2
    MQ = MessageQueue()  # queue
    part1() # 1020211150 (18950 low + 53837 high pulses)
    part2()  # 238815727638557 button presses