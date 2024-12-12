import sys


class Region:
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    def __init__(self, id: str, tile: tuple[int, int]) -> None:
        self.id = id
        self.tiles = [tile]

    def add_tile(self, tile):
        self.tiles.append(tile)

    def is_next_to(self, tile):

        for d in self.directions:
            if (tile[0] + d[0], tile[1] + d[1]) in self.tiles:
                return True

        return False

    def is_mergeable(self, other: "Region"):
        if self.id == other.id:
            for tile in self.tiles:
                if other.is_next_to(tile):
                    return True
        return False

    def merge(self, other):
        self.tiles.extend(other.tiles)
        return self

    def get_stats(self):
        perimeter = 0
        for tile in self.tiles:
            for d in self.directions:
                if (
                    not (
                        tile[0] + d[0],
                        tile[1] + d[1],
                    )
                    in self.tiles
                ):
                    perimeter += 1

        return perimeter, len(self.tiles)

    def populate_region(self, garden: list[str], tile: tuple[int, int]):
        rows, cols = len(garden), len(garden[0])
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        id = garden[tile[0]][tile[1]]
        for d in directions:
            new_tile = tile[0] + d[0], tile[1] + d[1]
            if (
                (0 <= new_tile[0] < rows)
                and (0 <= new_tile[1] < cols)
                and garden[new_tile[0]][new_tile[1]] == id
                and new_tile not in self.tiles
            ):
                self.add_tile(new_tile)
                self.populate_region(garden, new_tile)

    def __repr__(self) -> str:
        return f"id={self.id}, {self.tiles}"


def read_input(path) -> list[str]:
    with open(path, "r") as f:
        lines = f.read().strip().split("\n")

    return lines


def generate_regions(garden: list[str]) -> list[Region]:
    regions: list[Region] = []
    for i, row in enumerate(garden):
        for j, id in enumerate(row):
            tile = (i, j)

            found = False
            for region in regions:
                if tile in region.tiles:
                    found = True

            if not found:
                region = Region(id, tile)
                region.populate_region(garden, tile)
                regions.append(region)
    return regions


def fence_region_price(regions: list[Region]):
    price = 0
    for region in regions:
        perimeter, area = region.get_stats()
        price += perimeter * area

    return price


def main():
    garden = read_input(sys.argv[1])
    regions = generate_regions(garden)
    price = fence_region_price(regions)
    print(price)


if __name__ == "__main__":
    main()
