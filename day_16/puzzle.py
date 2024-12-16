import sys

directions = ((1, 0), (0, 1), (-1, 0), (0, -1))


class Node:

    def __init__(self, i, j, d, target=False) -> None:
        self.coords = self.i, self.j = i, j
        self.direction = d
        self.adjacent = []
        self.costs = []
        self.target = target

    def add_adjacent(self, other):
        if other not in self.adjacent:
            self.adjacent.append(other)
            if self.direction == other.direction:
                self.costs.append(1)
            else:
                self.costs.append(1000)

    def is_adjacent(self, other):
        for dx, dy in directions:
            if (self.coords[0] + dx == other.coords[0]) and (
                self.coords[1] + dy == other.coords[1]
            ):
                return True
        return False

    # Implement eq and hash for generating sets of nodes to find unique nodes
    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, type(self)):
            return (self.coords == value.coords) and (self.direction == value.direction)
        return False

    def __hash__(self) -> int:
        return hash((self.coords, self.direction))

    def __repr__(self) -> str:
        return f"coord={self.coords}, d={self.direction}, target={self.target}"


class Graph:

    def __init__(self, coords, start, end) -> None:
        self.start = Node(start[0], start[1], "e")
        self.ends = [Node(end[0], end[1], x, True) for x in directions]
        self.nodes = [self.start] + self.ends
        self.add_nodes(coords)

    def add_nodes(self, coords):
        for idx, coord in enumerate(coords):
            print(idx)
            for d in directions:
                node = Node(coord[0], coord[1], d)
                for other in self.nodes:
                    if node.is_adjacent(other):
                        node.add_adjacent(other)
                        other.add_adjacent(node)
                        self.nodes.append(node)

    def __repr__(self) -> str:
        pr = ""
        for node in self.nodes:
            pr += str(node) + "\n"
        return pr


def read_input(path):
    with open(path, "r") as f:
        lines = f.read().strip().split("\n")

    coords = []
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == "." or char == "S" or char == "E":
                if char == "E":
                    end = (i, j)
                elif char == "S":
                    start = (i, j)
                else:
                    coords.append((i, j))

    print(f"Found {len(coords)} nodes, creating graph")
    graph = Graph(coords, start, end)


def main():
    inp = read_input(sys.argv[1])
    print(inp)


if __name__ == "__main__":
    main()
