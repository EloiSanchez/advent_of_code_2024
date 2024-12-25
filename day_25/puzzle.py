from collections import defaultdict
import sys


def read_input(path):
    with open(path, "r") as f:
        lines = f.read().strip().split("\n")

    obj = None
    first_line = True
    keys, locks = [], []
    for line in lines:
        if first_line:
            if line == "#####":
                obj = "lock"
            else:
                obj = "key"
            cols = defaultdict(int)
            first_line = False

        else:
            if line.strip() == "":
                if obj == "lock":
                    locks.append([x for x in cols.values()])
                elif obj == "key":
                    keys.append([x - 1 for x in cols.values()])
                first_line = True
            else:
                for i, char in enumerate(line):
                    cols[i] += 1 if char == "#" else 0

    if obj == "lock":
        locks.append([x for x in cols.values()])
    elif obj == "key":
        keys.append([x - 1 for x in cols.values()])
    first_line = True
    return keys, locks


def unique_combinations(keys, locks):
    counter = 0
    for key in keys:
        for lock in locks:
            is_match = True
            for k, l in zip(key, lock):
                if k + l >= 6:
                    is_match = False
                    break

            if is_match:
                counter += 1
    return counter


def main():
    keys, locks = read_input(sys.argv[1])
    p1 = unique_combinations(keys, locks)
    print("P1:", p1)


if __name__ == "__main__":
    main()
