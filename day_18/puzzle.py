import sys
from functools import total_ordering

from tqdm import tqdm


directions = ((1, 0), (0, 1), (-1, 0), (0, -1))


@total_ordering
class Node:

    def __init__(self, i, j, start=False, target=False) -> None:
        self.coords = self.i, self.j = i, j
        self.target = target
        self.start = start
        self.prev: Node | None = None

        if self.start:
            self.distance = 0
        else:
            self.distance = None

    def get_back_path(self, path=None, distance=0) -> tuple[list["Node"], int]:
        """
        Recursively generate the path going to the previous nodes until it does not find
        one anymore or it reaches a node marked as start.
        """
        if path is None:
            path = []

        path.append(self)

        if self.start or self.prev is None:
            return path, distance

        distance += 1
        return self.prev.get_back_path(path, distance)

    # Implement eq and hash for generating sets of nodes to find unique nodes
    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, type(self)):
            return self.coords == value.coords
        return False

    def __hash__(self) -> int:
        return hash((self.coords))

    # Implement lt in order to create an orderable set of nodes based on distanc attr.
    def __lt__(self, other):
        if self.distance is not None:
            if other.distance is not None:
                return self.distance < other.distance
            return True
        elif other.distance is not None:
            return False
        return True

    def __repr__(self) -> str:
        return f"coord={self.coords}, d={self.distance}"


class Graph:

    def __init__(self, rows, cols) -> None:
        self.rows, self.cols = rows, cols
        self.num_elems = self.cols * self.rows
        self.reset()

    def reset(self):
        """
        Recreate attributes to set graph state as starting.
        """
        self.adjmat = [
            [0 for _ in range(self.num_elems)] for _ in range(self.num_elems)
        ]
        self.removed_coords = []
        self.map = [["." for _ in range(self.cols)] for _ in range(self.rows)]
        print("Creating adjacency matrix")
        for i in tqdm(range(self.rows)):
            for j in range(self.cols):
                for d in directions:
                    new_coord = (i + d[0], j + d[1])
                    if (0 <= new_coord[0] < self.rows) and (
                        0 <= new_coord[1] < self.cols
                    ):
                        self.adjmat[self._idx(i, j)][self._idx(*new_coord)] = 1

    def remove_corrupted_nodes(self, coords: list[tuple[int, int]]):
        """
        Remove corrupted nodes from the adjacency matrix
        """
        self.removed_coords = coords
        print("Removing corrupted nodes")
        for coord in tqdm(coords):
            r, c = coord
            self.adjmat[self._idx(r, c)] = [0 for _ in range(self.num_elems)]
            for i in range(self.num_elems):
                self.adjmat[i][self._idx(r, c)] = 0

    def dijkstra(self) -> tuple[list[Node], int]:
        """
        Implementation of Dijkstra's algorithm using pseudo-code and algorithm info
        from wikipedia https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
        """
        print("Starting Dijkstra")

        # Initialize variables
        unvisited: list[Node] = []
        nodes: list[list[Node | None]] = [
            [None for _ in range(self.cols)] for _ in range(self.rows)
        ]
        for i in range(self.rows):
            for j in range(self.cols):
                nodes[i][j] = Node(i, j)
                unvisited.append(nodes[i][j])

        unvisited[0].start = True
        unvisited[0].distance = 0
        unvisited[-1].target = True

        node = unvisited[0]
        while unvisited:

            # Sort unvisited nodes by distance
            unvisited.sort()

            # Visit new node
            node = unvisited.pop(0)

            # If no path is available
            if node.distance is None:
                raise ValueError("Could not find path from start to target")

            # If node is end
            if node.target:
                break

            # Find adjacents of current node
            i, j = node.coords
            for n_idx, is_neigh in enumerate(self.adjmat[self._idx(i, j)]):
                if is_neigh:
                    n_i, n_j = self._ridx(n_idx)
                    neigh = nodes[n_i][n_j]
                    if neigh in unvisited:
                        dist = node.distance + 1
                        if neigh.distance is None or neigh.distance < dist:
                            neigh.prev = node
                            neigh.distance = dist

        return node.get_back_path()

    def draw_path(self, path: list[Node]):
        map = self.get_map()
        for node in path:
            i, j = node.coords
            map[i][j] = "O"
        print("\n" + "\n".join(["".join(r) for r in map]))

    def get_map(self):
        map = self.map.copy()
        for coord in tqdm(self.removed_coords):
            r, c = coord
            map[r][c] = "#"
        return map

    def __repr__(self) -> str:
        return "\n" + "\n".join(["".join(r) for r in self.get_map()])

    def print_adjmat(self):
        print(
            "\n" + "\n".join(["".join(map(lambda x: str(x), r)) for r in self.adjmat])
        )

    def _idx(self, i, j):
        """Maps 2d coordinates to 1d coordinates"""
        return self.cols * i + j

    def _ridx(self, idx):
        """Maps 1d coordinates to 2d coordinates"""
        return int(idx // self.cols), idx % self.cols


def find_breaking_byte(coords: list[tuple[int, int]], graph: Graph):
    # Get first path
    graph.reset()
    path, _ = graph.dijkstra()
    graph.draw_path(path)

    used_coords = []
    for i, j in coords:
        used_coords.append((i, j))

        # If node in current path, it breaks it
        if Node(i, j) in path:
            try:
                # Find new path
                graph.reset()
                graph.remove_corrupted_nodes(used_coords)
                path, d = graph.dijkstra()
                print(f"{(i, j)=} Broke path. New distance: {d}")
                graph.draw_path(path)
            except ValueError:
                # If Dijkstra fails, current byte is the byte that removes all available
                # paths
                return (i, j)


def read_input(path, rows, columns):
    with open(path, "r") as f:
        lines = f.read().strip().split("\n")

    coords = []
    for line in lines:
        y, x = [int(v) for v in line.split(",")]
        coords.append((x, y))

    graph = Graph(rows, columns)

    return coords, rows, columns, graph


def main():
    coords, _, _, graph = read_input(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))

    # P1
    graph.remove_corrupted_nodes(coords[: int(sys.argv[4])])
    path, p1 = graph.dijkstra()
    graph.draw_path(path)

    # P2
    p2 = find_breaking_byte(coords, graph)

    print("\n\nP1: ", p1)
    print("P2 (reversed): ", p2)


if __name__ == "__main__":
    main()
