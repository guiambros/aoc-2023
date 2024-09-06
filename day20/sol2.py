from collections import defaultdict, deque


class Module:
    def __init__(self, name, output_modules):
        self.name = name
        self.output_modules = output_modules
        self.messages = deque()

    def receive_message(self, message, sender=None):
        self.messages.append(message)

    def send_message(self):
        # default to rebroadcasting first received message
        if self.messages:
            return self.messages.popleft()
        else:
            return None


class Flip_Flop(Module):
    def __init__(self, name, output_modules):
        super().__init__(name, output_modules)
        self.status = False

    def __repr__(self):
        return f"Flip Flop module {self.name}, output to {self.output_modules}, {'ON' if self.status else 'OFF'}"

    def receive_message(self, message, sender=None):
        super().receive_message(message, sender)
        if not message:
            # low pulse received
            self.status = not self.status

    def send_message(self):
        first_received = self.messages.popleft()
        if first_received:
            # do nothing for high pulse
            return None
        else:
            return self.status


class Conjunction(Module):
    def __init__(self, name, output_modules, input_modules):
        super().__init__(name, output_modules)
        self.input_modules = input_modules
        self.messages = defaultdict(lambda: False)

    def __repr__(self):
        return f"Conjunction module {self.name}, input from {self.input_modules} last received messages {self.messages}, output to {self.output_modules}"

    def receive_message(self, message, sender=None):
        self.messages[sender] = message

    def send_message(self):
        first_received = [self.messages[i] for i in self.input_modules]
        return not all(first_received)


class Broadcast(Module):
    def __init__(self, name, output_modules):
        super().__init__(name, output_modules)

    def __repr__(self):
        return f"Broadcast module output to {self.output_modules}"


class Output(Module):
    def __init__(self, name="output", output_modules=[]):
        super().__init__(name, output_modules)

    def __repr__(self):
        return "Output module."

    def send_message(self):
        return None


def make_graph(lines):
    inputs = defaultdict(list)
    outputs = defaultdict(list)

    for line in lines:
        line = line.split(" -> ")
        name, connected = line[0], line[1].split(", ")
        outputs[name] = connected

        for output in connected:
            inputs[output].append(name[1:] if name != "broadcaster" else name)

    return inputs, outputs


def make_modules(inputs, outputs):
    modules = {}
    for name, connected in outputs.items():
        match name[0]:
            case "b":
                modules["broadcaster"] = Broadcast("broadcaster", connected)
            case "%":
                modules[name[1:]] = Flip_Flop(name[1:], connected)
            case "&":
                modules[name[1:]] = Conjunction(name[1:], connected, inputs[name[1:]])

    modules["output"] = Output()
    return modules


def press_once(modules, log=False):
    to_process = deque(["broadcaster"])
    modules["broadcaster"].receive_message(False)
    num_low, num_high = 1, 0

    while to_process:
        processing = to_process.popleft()
        if processing not in modules:
            continue

        processing = modules[processing]
        to_send = processing.send_message()

        if to_send is not None:
            to_process.extend(processing.output_modules)

            for module in processing.output_modules:
                if to_send:
                    num_high += 1
                else:
                    num_low += 1

                if log:
                    print(f"{processing.name} -{'high' if to_send else 'low'}-> {module}")

                if module not in modules:
                    continue

                receiver = modules[module]
                receiver.receive_message(to_send, processing.name)

    return num_low, num_high


def main():
    with open("input_2023_20.txt", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]

    modules = make_modules(*make_graph(lines))
    num_presses = 1000
    num_low, num_high = 0, 0

    for i in range(num_presses):
        low_sent, high_sent = press_once(modules, True)
        num_low += low_sent
        num_high += high_sent

    print(num_low * num_high)
    return


main()
