from functools import cached_property

import numpy as np

OFFSETS = {
    # turn: {current_direction: (delta_row, delta_col)}
    "straight": {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)},
    "left": {"^": (0, -1), "v": (0, 1), "<": (1, 0), ">": (-1, 0)},
    "right": {"^": (0, 1), "v": (0, -1), "<": (-1, 0), ">": (1, 0)},
}
DIRECTION_LABEL = {
    (-1, 0): "^",
    (1, 0): "v",
    (0, -1): "<",
    (0, 1): ">",
}


class Map:
    def __init__(self, data, max_path_length=0):
        self.data = data
        self.max_path_length = max_path_length

    @cached_property
    def rows(self):
        return self.data.shape[0]

    @cached_property
    def cols(self):
        return self.data.shape[1]

    @cached_property
    def start(self):
        return 0, next(i for i, x in enumerate(self.data[0, :]) if x == ".")

    @cached_property
    def end(self):
        return self.rows - 1, next(
            i for i, x in enumerate(self.data[self.rows - 1, :]) if x == "."
        )

    @staticmethod
    def get_neighbor(loc, offset):
        return loc[0] + offset[0], loc[1] + offset[1]

    def is_valid(self, loc, direction):
        # Assume all borders of the grid are closed
        # Valid neighbors are non "#"
        return (
            1 <= loc[0] < self.rows - 1
            and 1 <= loc[1] < self.cols - 1
            and self.data[loc] in "<>v^."
            and (self.data[loc] == direction or self.data[loc] == ".")
        ) or loc == self.end

    def find_path(self, parent, steps, direction, visited_nodes):
        if parent in visited_nodes:
            return
        orig_parent = parent
        neighbor_next_dir = []

        while True:
            if orig_parent == parent:
                neighbor_next_dir.append(
                    (
                        (
                            neighbor := self.get_neighbor(
                                parent, (offset := OFFSETS["straight"][direction])
                            )
                        ),
                        DIRECTION_LABEL[offset],
                    )
                )

            else:
                for turn in ["straight", "left", "right"]:
                    if self.is_valid(
                        (
                            neighbor := self.get_neighbor(
                                parent,
                                (offset := OFFSETS[turn][direction]),
                            )
                        ),
                        next_dir := DIRECTION_LABEL[offset],
                    ):
                        neighbor_next_dir.append((neighbor, next_dir))
                        if neighbor == self.end:
                            self.max_path_length = max(self.max_path_length, steps)
                            return

            if len(neighbor_next_dir) == 1:
                parent, direction = neighbor_next_dir[0]
                neighbor_next_dir = []
                steps += 1
                continue

            break
        visited_nodes.append(orig_parent)
        for _, d in neighbor_next_dir:
            self.find_path(parent, steps, d, visited_nodes.copy())


if __name__ == "__main__":
    with open("day_23/input.txt") as f:
        array = np.array([list(x) for x in f.read().split()])

    aoc_map = Map(array)
    aoc_map.find_path(aoc_map.start, 1, "v", [])
    print(f"PART 1: {aoc_map.max_path_length}")

    aoc_map = Map(np.where(np.isin(array, list("<>v^")), ".", array))
    aoc_map.find_path(aoc_map.start, 1, "v", [])
    print(f"PART 2: {aoc_map.max_path_length}")
