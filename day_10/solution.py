import numpy as np
from skspatial.measurement import area_signed


class Tile:
    grid = None

    def __init__(self, row, col, parent_from=""):
        self.row = row
        self.col = col
        self.parent_from = parent_from

    def __lt__(self, other):
        return self.col < other.col

    @property
    def char(self):
        return self.grid.data[self.row, self.col]

    def __repr__(self):
        return f"Tile({self.row}, {self.col}, {self.char}, {self.parent_from})"

    @property
    def north(self):
        return Tile(self.row - 1, self.col, parent_from="south")

    @property
    def south(self):
        return Tile(self.row + 1, self.col, parent_from="north")

    @property
    def west(self):
        return Tile(self.row, self.col - 1, parent_from="east")

    @property
    def east(self):
        return Tile(self.row, self.col + 1, parent_from="west")


class Grid:
    def __init__(self, data):
        self.data = data

    @property
    def start(self):
        index_s = np.where(self.data == "S")
        return Tile(index_s[0][0], index_s[1][0])

    def get_adjacent(self, parent):
        match parent.char:
            case "|":
                return parent.north if parent.parent_from == "south" else parent.south
            case "L":
                return parent.north if parent.parent_from == "east" else parent.east
            case "J":
                return parent.north if parent.parent_from == "west" else parent.west
            case "7":
                return parent.south if parent.parent_from == "west" else parent.west
            case "F":
                return parent.south if parent.parent_from == "east" else parent.east
            case "-":
                return parent.west if parent.parent_from == "east" else parent.east
            case "S":
                if parent.north.char in ["|", "7", "F"]:
                    return parent.north
                if parent.south.char in ["|", "L", "J"]:
                    return parent.south
                if parent.west.char in ["-", "L", "F"]:
                    return parent.west
                if parent.east.char in ["-", "J", "7"]:
                    return parent.east


if __name__ == "__main__":
    with open("day_10/input.txt") as f:
        grid = Grid(np.array([list(x) for x in f.read().split()]))

    Tile.grid = grid
    next_tile = grid.get_adjacent(grid.start)
    tile_loop = [(next_tile.row, next_tile.col)]
    while next_tile.char != "S":
        next_tile = grid.get_adjacent(next_tile)
        tile_loop.append((next_tile.row, next_tile.col))

    print(f"PART 1: {len(tile_loop) // 2}")
    # area_signed implements the shoelace algorithm to calculate are inside polygon
    print(f"PART 2: {int(abs(area_signed(tile_loop)) + 1 - len(tile_loop) / 2)}")
