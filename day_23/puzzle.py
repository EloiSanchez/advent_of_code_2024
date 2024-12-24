from itertools import combinations
import sys
from typing import Iterable


class Graph:

    def __init__(self) -> None:
        self.nodes = {}
        self.names = {}
        self.elements = 0
        self.adjmat = []

    def add_node(self, name: str):
        if name not in self.nodes:
            self.nodes[name] = self.elements
            self.names[self.elements] = name
            self.elements += 1

    def add_connection(self, name_1: str, name_2: str):
        if not self.adjmat:
            self.adjmat = [
                [0 for _ in range(self.elements)] for _ in range(self.elements)
            ]
        i, j = self.nodes[name_1], self.nodes[name_2]
        self.adjmat[i][j] = 1
        self.adjmat[j][i] = 1

    def connected_to(self, idx: int):
        connections = []
        for i, neigh in enumerate(self.adjmat[idx]):
            if neigh:
                connections.append(i)

        return connections

    def groups_of(self, n: int) -> Iterable[list[str]]:
        given = []
        for i, r in enumerate(self.adjmat):
            if sum(r) >= n - 1 and i not in given:
                for node_1, node_2 in combinations(self.connected_to(i), 2):
                    if self.adjmat[node_1][node_2]:
                        group = set((i, node_1, node_2))
                        if group not in given:
                            given.append(group)
                            yield [self.names[x] for x in (i, node_1, node_2)]


def read_input(path):
    with open(path, "r") as f:
        lines = f.read().strip().split("\n")

    pairs = []
    for line in lines:
        pairs.append(line.split("-"))
    return pairs


def find_groups(connections: list[tuple[str, str]]):
    graph = Graph()
    for pc1, pc2 in connections:
        graph.add_node(pc1)
        graph.add_node(pc2)

    for pc1, pc2 in connections:
        graph.add_connection(pc1, pc2)

    return graph


def count_p1(graph: Graph):
    p1 = 0
    for group in graph.groups_of(3):
        if any(x[0] == "t" for x in group):
            p1 += 1
    return p1


def main():
    pairs = read_input(sys.argv[1])
    groups = find_groups(pairs)
    p1 = count_p1(groups)
    print("P1: ", p1)


if __name__ == "__main__":
    main()
