from dataclasses import dataclass
from itertools import combinations
from typing import ClassVar

import numpy as np

PART = 2


@dataclass
class Galaxy:
    row: int
    col: int
    no_galaxy_rows: ClassVar[tuple]
    no_galaxy_cols: ClassVar[tuple]
    expansion_offset: ClassVar[tuple]

    def __sub__(self, other):
        lower_row, higher_row = sorted((self.row, other.row))
        lower_col, higher_col = sorted((self.col, other.col))
        expansion = 0
        for no_galaxy_row in self.no_galaxy_rows:
            if no_galaxy_row in range(lower_row, higher_row):
                expansion += self.expansion_offset
        for no_galaxy_col in self.no_galaxy_cols:
            if no_galaxy_col in range(lower_col, higher_col):
                expansion += self.expansion_offset
        return higher_row - lower_row + higher_col - lower_col + expansion


if __name__ == "__main__":
    with open("day_11/input.txt") as f:
        data = np.array([list(x) for x in f.read().split()])

    galaxy_rows, galaxy_cols = np.where(data == "#")

    Galaxy.no_galaxy_rows = tuple(
        i for i in range(data.shape[0]) if i not in galaxy_rows
    )
    Galaxy.no_galaxy_cols = tuple(
        i for i in range(data.shape[1]) if i not in galaxy_cols
    )
    Galaxy.expansion_offset = 999_999 if PART == 2 else 1

    galaxies = [Galaxy(*x) for x in zip(galaxy_rows, galaxy_cols)]
    print(f"PART_{PART} = {sum(x - y for x, y in combinations(galaxies, 2))}")
