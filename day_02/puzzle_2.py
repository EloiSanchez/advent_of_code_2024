from puzzle_1 import read_input, is_safe


def problem_dampener(lines: list[list[int]]):
    count_safe = 0
    for line in lines:
        if is_safe(line):
            count_safe += 1
        else:
            for idx, _ in enumerate(line):
                line_copy = line.copy()
                line_copy.pop(idx)
                if is_safe(line_copy):
                    count_safe += 1
                    break

    return count_safe


def main():
    lines = read_input("input.txt")
    safe_count = problem_dampener(lines)
    print(safe_count)


if __name__ == "__main__":
    main()
