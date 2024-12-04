from typing import Iterable
import numpy as np


def read_input(path):
    with open(path, "r") as f:
        return f.readlines()


def check_slice(arr: Iterable, word: str) -> bool:
    return "".join(arr) == word


def count_word(text: list[str], word: str):
    arr = np.array([[x for x in row.strip()] for row in text])
    rows, columns = arr.shape
    len_word = len(word)
    count = 0
    for i in range(rows):
        for j in range(columns):
            slices = []

            slices.append(arr[i : i + len_word, j])  # Column up to down
            slices.append(
                arr[rows - (i + len_word) : rows - i, j][::-1]
            )  # Column down to up
            slices.append(arr[i, j : j + len_word])  # Row lef to right
            slices.append(
                arr[i, columns - (j + len_word) : columns - j][::-1]
            )  # Row right to left

            sub_arr = arr[
                i : i + len_word, j : j + len_word
            ]  # Get subarray for diagonals
            slices.append(sub_arr.diagonal())  # Main diagonal
            slices.append(np.fliplr(sub_arr).diagonal())  # Opposite diagonal
            slices.append(sub_arr.diagonal()[::-1])  # Main diagonal inverted
            slices.append(
                np.fliplr(sub_arr).diagonal()[::-1]
            )  # Opposite diagonal inverted

            for slice in slices:
                count += 1 if check_slice(slice, word) else 0

    return count


def main():
    text = read_input("input.txt")
    xmas_count = count_word(text, "XMAS")
    print(xmas_count)


if __name__ == "__main__":
    main()
