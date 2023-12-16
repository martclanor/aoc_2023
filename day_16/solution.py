from dataclasses import dataclass
from typing import ClassVar

import numpy as np


@dataclass(slots=True)
class Beam:
    row_index: int
    col_index: int
    direction: str
    layout: ClassVar[np.array]
    extra: ClassVar[list]
    members: ClassVar[set]

    def __hash__(self):
        return hash((self.row_index, self.col_index))

    def __eq__(self, other):
        return (
            self.row_index == other.row_index
            and self.col_index == other.col_index
            and self.direction == other.direction
        )

    def move(self):
        if self in self.members:
            return None

        # Register all beams that "moves"
        self.members.add(self)

        # Find location of next beam based on current beam direction
        match self.direction:
            case "u":
                r, c = self.row_index - 1, self.col_index
            case "d":
                r, c = self.row_index + 1, self.col_index
            case "l":
                r, c = self.row_index, self.col_index - 1
            case "r":
                r, c = self.row_index, self.col_index + 1

        # Ignore beam if outside the layout
        if r < 0 or c < 0 or r == self.layout.shape[0] or c == self.layout.shape[1]:
            return None

        # Find direction of next beam
        symbol = self.layout[r, c]
        match symbol:
            case ".":
                d = self.direction
            case "/":
                match self.direction:
                    case "u":
                        d = "r"
                    case "d":
                        d = "l"
                    case "l":
                        d = "d"
                    case "r":
                        d = "u"
            case "\\":
                match self.direction:
                    case "u":
                        d = "l"
                    case "d":
                        d = "r"
                    case "l":
                        d = "u"
                    case "r":
                        d = "d"
            case "-":
                match self.direction:
                    case "u" | "d":
                        d = "l"
                        # When beam is split, keep one in extra and loop through later
                        self.extra.append(Beam(r, c, "r"))
                    case "l" | "r":
                        d = self.direction
            case "|":
                match self.direction:
                    case "u" | "d":
                        d = self.direction
                    case "l" | "r":
                        d = "u"
                        # When beam is split, keep one in extra and loop through later
                        self.extra.append(Beam(r, c, "d"))

        return Beam(r, c, d)


def count_energized(beam):
    # For each beam start, reinitialize class variables
    Beam.extra = []
    Beam.members = set()
    while True:
        while beam:
            beam = beam.move()
        if beams := Beam.extra:
            beam = beams.pop(0)
            continue
        break
    return len(set((x.row_index, x.col_index) for x in Beam.members)) - 1


if __name__ == "__main__":
    with open("day_16/input.txt") as f:
        data = np.array([list(x) for x in f.read().split()])

    Beam.layout = data

    print(f"PART 1: {count_energized(Beam(0, -1, 'r'))}")

    counter = []
    rows, cols = Beam.layout.shape
    for row in range(rows):
        counter.append(count_energized(Beam(row, -1, "r")))
        counter.append(count_energized(Beam(row, cols, "l")))

    for col in range(cols):
        counter.append(count_energized(Beam(-1, col, "d")))
        counter.append(count_energized(Beam(rows, col, "u")))

    print(f"PART 2: {max(counter)}")
