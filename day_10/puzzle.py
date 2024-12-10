from collections import defaultdict
import sys


class Node:

    def __init__(
        self, height: int, i: int, j: int, previous: "Node | None" = None
    ) -> None:
        super().__init__()

        # Constant parameters
        self.coords = self.i, self.j = i, j
        self.height = height

        # Add previous node
        self.previous_node = None
        self.path = [self]
        if previous is not None:
            self.previous_node = previous
            self.path = previous.path + self.path
            previous.add_next(self)

        # New nodes starts empty, will be added in init of next node
        self.next_nodes = []

    # Implement eq and hash for generating sets of nodes to find unique nodes
    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, type(self)):
            return (self.coords == value.coords) and (self.height == value.height)
        return False

    def __hash__(self) -> int:
        return hash((self.coords, self.height))

    # Called on initialization of next node
    def add_next(self, other: "Node"):
        self.next_nodes.append(other)

    # For debugging
    def __repr__(self) -> str:
        return f"height={self.height}, coords={self.coords}"

    def print_path(self, rows, columns):
        map: list[list] = [["." for _ in range(columns)] for _ in range(rows)]
        for node in self.path:
            map[node.i][node.j] = node.height
        print(f"\n{self}")
        for row in map:
            print("".join(str(x) for x in row))


def read_input(path):
    with open(path, "r") as f:
        lines = f.read().strip().split("\n")
    return [[int(x) for x in line] for line in lines]


def find_trails(map: list[list[int]]):
    trailheads = {}
    for i, row in enumerate(map):
        for j, height in enumerate(row):

            # Trails only need to be found on starting points with height 0
            if height == 0:
                node = Node(height, i, j)
                endings = []
                find_trail(i, j, map, node, endings)

                # Get last nodes of all paths found for this trailhead
                trailheads[(i, j)] = endings

    return trailheads


def find_trail(i: int, j: int, map: list[list[int]], node: Node, endings: list):
    # If end of trail
    if node.height == 9:
        endings.append(node)
        return

    # For each new direction found, create a node and continue finding trail from there
    for new_i, new_j in find_next_step(i, j, map):
        new_node = Node(map[new_i][new_j], new_i, new_j, node)
        find_trail(new_i, new_j, map, new_node, endings)


def find_next_step(i: int, j: int, map: list[list[int]]):
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    for direction in directions:
        new_i, new_j = new_pos = i + direction[0], j + direction[1]
        if (
            (0 <= new_i < len(map))
            and (0 <= new_j < len(map[0]))
            and map[i][j] + 1 == map[new_i][new_j]
        ):
            yield new_pos


def count_scores(trails):
    count = 0
    rating = 0
    for nodes in trails.values():
        rating += len(nodes)
        count += len(set(nodes))
    return count, rating


def main():
    map = read_input(sys.argv[1])
    # print(map)

    trails = find_trails(map)
    # Print found paths
    # for node in trails[(i, j)]:
    #     node.print_path(len(map), len(map[0]))

    score, rating = count_scores(trails)
    print("Puzzle 1:", score, "  Puzzle 2:", rating)


if __name__ == "__main__":
    main()
