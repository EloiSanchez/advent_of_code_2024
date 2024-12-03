import re

from puzzle_1 import read_input, sum_patterns


def find_pattern(text):
    mul_pattern = re.compile(r"mul\([\d]{1,3},[\d]{1,3}\)")
    do_pattern = re.compile(r"do\(\)|don\'t\(\)")

    return mul_pattern.finditer(text), [x for x in do_pattern.finditer(text)]


def parse_commands(mul_matches, do_matches):

    active_muls = []
    for mul_match in mul_matches:
        if is_active(mul_match, do_matches):
            active_muls.append(mul_match[0])
    return active_muls


def is_active(mul_match, do_matches):
    mul_start = mul_match.start()
    active = True
    for do_match in do_matches:
        if mul_start < do_match.start():
            break
        active = True if do_match[0] == "do()" else False

    return active


def main():
    text = read_input("input.txt")
    mul_matches, do_matches = find_pattern(text)
    active_muls = parse_commands(mul_matches, do_matches)
    total_sum = sum_patterns(active_muls)
    print(total_sum)


if __name__ == "__main__":
    main()
