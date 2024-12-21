import sys
from collections import deque


cache = {}
directions = {(0, -1): "<", (1, 0): "v", (-1, 0): "^", (0, 1): ">"}


class NumPad:
    dirs = {(0, -1): "<", (1, 0): "v", (-1, 0): "^", (0, 1): ">"}

    def __init__(self) -> None:
        self.pad: list[list[str | None]] = [
            ["7", "8", "9"],
            ["4", "5", "6"],
            ["1", "2", "3"],
            [None, "0", "A"],
        ]
        self.rows = len(self.pad)
        self.cols = len(self.pad[0])
        self.i: int = 3
        self.j: int = 2

    def press_button(self, start, val: str):
        """
        Breath First Search implementation to find all paths to a button and then choose
        the most optimized for subsequent robots.
        """
        Q = deque([(start[0], start[1], "")])
        seen = set()
        ways = []
        while Q:
            i, j, dirs = Q.popleft()
            seen.add((i, j))
            if self.get_val(i, j) == val:
                self.i, self.j = i, j
                ways.append(dirs + "A")

            for d, v in self.dirs.items():
                ni, nj = i + d[0], j + d[1]
                if (
                    (0 <= ni < self.rows)
                    and (0 <= nj < self.cols)
                    and ((ni, nj) not in seen)
                    and self.get_val(i, j) is not None
                ):
                    Q.append((ni, nj, dirs + v))

        return sorted(ways, key=sort)[0]

    def press_sequence(self, sequence: str):
        """Find directions for multiple button presses"""
        dirs = ""
        for code in sequence:
            dirs += self.press_button((self.i, self.j), code)
        return dirs

    def get_val(self, i, j):
        return self.pad[i][j]

    def change_state(self, val):
        for i, row in enumerate(self.pad):
            for j, char in enumerate(row):
                if char == val:
                    self.i, self.j = i, j
                    return


def read_input(path):
    with open(path, "r") as f:
        lines = f.read().strip().split("\n")
    return lines


def sort(seq):
    """Used to sort sequences for most optimal."""
    # Less changes of keys is better
    changes = 0
    for i in range(len(seq) - 1):
        if seq[i] != seq[i + 1]:
            changes += 1

    # If we can choose to start in the left, is better, beacause is the
    # furthest away
    val = ""
    if seq[0] == "<":
        val += "0"
    else:
        val += "1"

    # In case of same changes, choose the one that starts going left
    return str(changes) + val


def find_complexity(codes, intermediate_robots: int):
    # Initialize robots
    numpad = NumPad()
    keypad = [[None, "^", "A"], ["<", "v", ">"]]

    p1 = 0
    for code in codes:
        seq = numpad.press_sequence(code)
        i, j = 0, 2
        length = 0
        for char in seq:
            l, i, j = press_button((i, j), char, keypad, intermediate_robots + 1)
            length += l

        # Calculate complexity
        num = int(code[:-1])
        p1 += length * num

    return p1


def press_button(start, val, pad, N):
    """
    Breath First Search implementation to find all paths to a button and then choose
    the most optimized for subsequent robots. Call again with the new sequence and
    repeat for each of the robots in the middle layer.
    """

    # If cached, avoid calculation
    if (start, val, N) in cache:
        return cache[(start, val, N)]

    # Intialize bfs
    Q = deque([(start[0], start[1], "")])
    seen = set()
    ways = []
    f_i, f_j = None, None

    # bfs loop
    while Q:
        i, j, dirs = Q.popleft()
        seen.add((i, j))
        if pad[i][j] == val:
            f_i, f_j = i, j
            ways.append(dirs + "A")

        for d, v in directions.items():
            ni, nj = i + d[0], j + d[1]
            if (
                (0 <= ni < len(pad))
                and (0 <= nj < len(pad[0]))
                and ((ni, nj) not in seen)
                and pad[i][j] is not None
            ):
                Q.append((ni, nj, dirs + v))

    # Find most optimal sequence
    seq = sorted(ways, key=sort)[0]

    # If not last robot, call again for each of the elements of the sequence
    if N == 1:
        result = len(seq)
    else:
        result = 0
        i, j = 0, 2
        for x in seq:
            length, i, j = press_button((i, j), x, pad, N - 1)
            result += length

    # Save in cache and return
    cache[(start, val, N)] = result, f_i, f_j
    return result, f_i, f_j


def main():
    codes = read_input(sys.argv[1])
    p1 = find_complexity(codes, intermediate_robots=1)
    p2 = find_complexity(codes, intermediate_robots=24)
    print("P1: ", p1, "P2: ", p2)


if __name__ == "__main__":
    main()
