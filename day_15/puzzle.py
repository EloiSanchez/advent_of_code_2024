import sys
import time


def read_input(path):
    with open(path, "r") as f:
        lines = f.read().strip().split("\n")

    map = {}
    phase = 1
    moves = ""
    for i, line in enumerate(lines):
        if phase == 1:
            if line.strip() == "":
                phase += 1
            else:
                for j, c in enumerate(line):
                    if c == "@":
                        pos = (i, j)
                    map[(i, j)] = c
        elif phase == 2:
            moves += line

    return pos, map, moves


def solve_moves(
    pos: tuple[int, int], map: dict[tuple[int, int], str], moves: list[str]
):
    for move in moves:
        new_pos, moved = do_move(pos, map, move)
        if moved:
            pos = new_pos
        # print_map(pos, map)
        # time.sleep(0.5)

    return pos, map


def do_move(pos: tuple[int, int], map: dict[tuple[int, int], str], move: str):
    dirs = {"^": (-1, 0), "v": (1, 0), ">": (0, 1), "<": (0, -1)}
    dir = dirs[move]

    # print(f"Trying to move {move} object {map[pos]}")
    new_pos = (pos[0] + dir[0], pos[1] + dir[1])
    if map[new_pos] == "O":
        # print(f"Box found, trying to move it")
        _, can_move = do_move(new_pos, map, move)
    elif map[new_pos] == "#":
        # print(f"Wall found, cannot move")
        can_move = False
    else:
        # print(f"Nothing found, moving")
        can_move = True
    if can_move:
        map[new_pos] = map[pos]
        map[pos] = "."
    return new_pos, can_move


def gps_sum(map):
    ans = 0
    for (i, j), c in map.items():
        if c == "O":
            ans += 100 * i + j
    return ans


def print_map(robot, map):
    rows, cols = 0, 0
    for k in map:
        rows = max(rows, k[0])
        cols = max(cols, k[1])

    to_print = [[0 for _ in range(cols + 1)] for _ in range(rows + 1)]

    for pos, c in map.items():
        to_print[pos[0]][pos[1]] = c

    to_print[robot[0]][robot[1]] = "@"

    pr = ""
    for r in to_print:
        for c in r:
            pr += c
        pr += "\n"
    print(pr)


def main():
    robot, map, moves = read_input(sys.argv[1])
    _, map = solve_moves(robot, map, moves)
    p1 = gps_sum(map)
    print(p1)


if __name__ == "__main__":
    main()
