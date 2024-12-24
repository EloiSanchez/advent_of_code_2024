from collections import deque
import sys


def read_input(path):
    with open(path, "r") as f:
        lines = f.read().strip().split("\n")

    phase_1 = True
    wires = {}
    operations = []
    for line in lines:
        if line.strip() == "":
            phase_1 = False
            continue

        if phase_1:
            wire, value = [x.strip() for x in line.split(":")]
            wires[wire] = int(value)

        else:
            operation, output = line.split(" -> ")
            operations.append(operation.split() + [output])

    return wires, deque(operations)


def make_operations(wires: dict[str, int], operations: deque):
    while operations:
        wire_1, op, wire_2, out = operation = operations.popleft()
        try:
            wires[out] = make_operation(wires, wire_1, op, wire_2)
        except KeyError:
            operations.append(operation)

    return wires


def make_operation(wires: dict[str, int], wire_1: str, op: str, wire_2: str):
    if op == "AND":
        return int(wires[wire_1] and wires[wire_2])
    elif op == "XOR":
        return wires[wire_1] ^ wires[wire_2]
    elif op == "OR":
        return int(wires[wire_1] or wires[wire_2])
    else:
        raise ValueError(f"Unknown operator {op}")


def to_decimal(wires: dict[str, int]):
    res = ""
    outs = list(wires.keys())
    outs.sort()
    for out in outs:
        if out[0] == "z":
            res = str(wires[out]) + res

    return int(res, base=2)


def main():
    wires, operations = read_input(sys.argv[1])
    wires = make_operations(wires, operations)
    p1 = to_decimal(wires)
    print(p1)


if __name__ == "__main__":
    main()
