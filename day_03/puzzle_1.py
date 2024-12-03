import re


def read_input(path):
    f = open(path, "r")
    return " ".join(f.read().split("\n"))


def find_pattern(text):
    pattern = re.compile(r"mul\([\d]{1,3},[\d]{1,3}\)")
    return pattern.findall(text)


def sum_patterns(patterns):
    return sum(
        [
            y * z
            for y, z in map(lambda x: [int(a) for a in x[4:-1].split(",")], patterns)
        ]
    )


def main():
    text = read_input("input.txt")
    patterns = find_pattern(text)
    total_sum = sum_patterns(patterns)
    print(total_sum)


if __name__ == "__main__":
    main()
