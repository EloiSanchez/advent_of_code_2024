import numpy as np
from puzzle_1 import read_input, check_slice


def xword_count(text, word):
    arr = np.array([[x for x in row.strip()] for row in text])
    rows, columns = arr.shape
    len_word = len(word)
    count = 0
    for i in range(rows):
        for j in range(columns):
            slices = []

            sub_arr = arr[i : i + len_word, j : j + len_word]
            slices.append(sub_arr.diagonal())  # Main diagonal
            slices.append(np.fliplr(sub_arr).diagonal())  # Opposite diagonal
            slices.append(sub_arr.diagonal()[::-1])  # Main diagonal inverted
            slices.append(
                np.fliplr(sub_arr).diagonal()[::-1]
            )  # Opposite diagonal inverted

            if sum(check_slice(slice, word) for slice in slices) >= 2:
                count += 1

    return count


def main():
    text = read_input("input.txt")
    xmas_count = xword_count(text, "MAS")
    print(xmas_count)


if __name__ == "__main__":
    main()
