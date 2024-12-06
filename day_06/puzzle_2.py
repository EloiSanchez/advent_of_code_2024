import sys

from puzzle_1 import read_input, find_travelled_area


def find_loops(map, agent_pos):
    loops = []
    for i in range(len(map)):
        for j in range(len(map[0])):

            # Add obstacle to position i, j
            new_map = []
            for row in map:
                new_map.append(row.copy())
            new_map[i][j] = 1

            # See if agent gets stuck in loop
            pos = agent_pos
            _, is_loop = find_travelled_area(new_map, pos)
            loops.append(is_loop)

    return sum(loops)


def main():
    map, agent_pos = read_input(sys.argv[1])

    loops = find_loops(map, agent_pos)
    print(loops)


if __name__ == "__main__":
    main()
