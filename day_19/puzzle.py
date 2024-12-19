import sys


def read_input(path):
    with open(path, "r") as f:
        lines = f.read().strip().split("\n")

    available = []
    todo = []
    for line in lines:
        if line == "":
            continue
        elif "," in line:
            available = [x.strip() for x in line.split(",")]
        else:
            todo.append(line)

    return available, todo


def count_possible(available: list[str], todo: list[str]) -> tuple[int, int]:
    count, possibles = 0, 0
    for pattern in todo:
        possibilities = count_patterns(available, pattern)
        if possibilities != 0:
            possibles += 1
        count += possibilities
    return possibles, count


cache = {}


def count_patterns(available: list[str], pattern: str) -> int:

    # If pattern pre-calculated, skip it
    if pattern in cache:
        return cache[pattern]

    # Base case
    if pattern == "":
        return 1

    # Find new patterns
    new_pats = []
    for av in available:
        if pattern.startswith(av):
            new_pat = pattern[len(av) :]
            new_pats.append(new_pat)

    # Call again for new patterns
    count = sum(count_patterns(available, x) for x in new_pats)

    # Save result in cache for this pattern
    cache[pattern] = count

    return count


def main():
    available, todo = read_input(sys.argv[1])
    p1, p2 = count_possible(available, todo)
    print("P1: ", p1)
    print("P2: ", p2)


if __name__ == "__main__":
    main()
