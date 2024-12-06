from collections import defaultdict
import sys


def read_input(path):
    with open(path, "r") as f:
        lines = f.read().strip().split("\n")

    obstacles = []
    for i, line in enumerate(lines):
        row = []
        for j, char in enumerate(line):
            row.append(1 if char == "#" else 0)
            if char not in ("#", "."):
                agent_pos = (i, j)
        obstacles.append(row)

    return obstacles, agent_pos


def valid_pos(pos, map):
    return


def get_new_pos(pos, directions, direction, idx, n_rows, n_cols, map):

    # New position
    next_pos = (
        pos[0] + directions[idx][0],
        pos[1] + directions[idx][1],
    )

    # Check if new position is between bounds and collides and change direction
    if (
        (0 <= next_pos[0] < n_rows)
        and (0 <= next_pos[1] < n_cols)
        and map[next_pos[0]][next_pos[1]]
    ):
        direction += 1
        idx = direction % 4
        try:
            return get_new_pos(pos, directions, direction, idx, n_rows, n_cols, map)
        except RecursionError:
            for m in map:
                print(m)
            print(pos)
            quit()

    return next_pos, direction, idx


def find_travelled_area(map, agent_pos):
    directions = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}
    states = defaultdict(list)

    n_rows = len(map)
    n_cols = len(map[0])

    idx, direction = 0, 0
    is_loop = False

    # Walk until we finish
    while True:

        # Save position AND direction
        states[agent_pos].append(idx)

        # Get new position
        agent_pos, direction, idx = get_new_pos(
            agent_pos, directions, direction, idx, n_rows, n_cols, map
        )

        # Agent leaves map
        if not (0 <= agent_pos[0] < n_rows) or not (0 <= agent_pos[1] < n_cols):
            break

        # Agent returns to a previously visited state
        elif idx in states[agent_pos]:
            is_loop = True
            break

    return len(states), is_loop


def main():
    map, agent_pos = read_input(sys.argv[1])
    travelled, _ = find_travelled_area(map, agent_pos)
    print(travelled)


if __name__ == "__main__":
    main()
