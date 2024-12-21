import sys

from collections import deque

directions = ((-1, 0), (0, 1), (1, 0), (0, -1))


def read_input(path):
    with open(path, "r") as f:
        lines = f.read().strip().split("\n")

    skips = set()
    for i, line in enumerate(lines):
        if "." in line:
            for j, char in enumerate(line):
                if j != 0 and j + 1 != len(line):
                    if char == "S":
                        start = (i, j)
                    print(i, j, char)
                    if char in ".SE":
                        for d in directions:
                            possible_skip = (i + d[0], j + d[1])
                            if is_skip(possible_skip, d, lines):
                                skips.add(possible_skip)

    return lines, skips, start


def is_skip(position: tuple[int, int], d: tuple[int, int], map: list[str]) -> bool:
    i, j = position
    ni, nj = i + d[0], j + d[1]

    if map[i][j] != "#":
        return False

    if (0 <= ni < len(map)) and (0 <= nj < len(map[0])) and map[ni][nj] == ".":
        return True

    return False


def bfs(
    start: tuple[int, int],
    map: list[str],
):
    # Nodeas are (row, column, distance from start)
    i, j, d = *start, 0
    queue = deque([(i, j, d)])
    seen = set()

    # Do bfs
    while queue:
        node = queue.popleft()
        for dir in directions:
            new_node = node[0] + dir[0], node[1] + dir[1]
            char = map[new_node[0]][new_node[1]]
            if char == ".":
                x, y, d = *new_node, node[2] + 1
                if (x, y) not in seen:
                    queue.append((x, y, d))
                    seen.add((x, y))
            elif char == "E":
                return node[2] + 1

    raise RuntimeError("Did not found path to end.")


def count_skips(start: tuple[int, int], map: list[str], skips: set[tuple[int, int]]):
    ps0 = bfs(start, map)

    p1 = 0
    for skip in skips:
        skipped_map = map.copy()
        row = skipped_map[skip[0]]
        new_row = ""
        for i, char in enumerate(row):
            if i == skip[1]:
                new_row += "."
            else:
                new_row += char
        skipped_map[skip[0]] = new_row

        ps = bfs(start, skipped_map)

        if ps0 - ps >= 100:
            p1 += 1

    return p1


def main():
    map, skips, start = read_input(sys.argv[1])
    new_map = map.copy()
    for skip in skips:
        line = new_map[skip[0]]
        new_line = ""
        for i, c in enumerate(line):
            if i == skip[1]:
                new_line += "X"
            else:
                new_line += c
        new_map[skip[0]] = new_line

    p1 = count_skips(start, map, skips)
    print(p1)


if __name__ == "__main__":
    main()
