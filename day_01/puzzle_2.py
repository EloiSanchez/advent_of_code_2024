from typing import DefaultDict
from puzzle_1 import read_input


def get_similarity(list_1, list_2):
    counter = DefaultDict(lambda: 0)
    for item in list_2:
        counter[item] += 1

    similarity = 0
    for item in list_1:
        similarity += item * counter[item]

    return similarity


def main():
    list_1, list_2 = read_input("input_1.txt")

    similarity = get_similarity(list_1, list_2)

    print(similarity)


if __name__ == "__main__":
    main()
