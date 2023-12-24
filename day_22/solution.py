from dataclasses import dataclass

import numpy as np
from tqdm import tqdm


@dataclass
class Cube:
    x: int
    y: int
    z: int

    def move(self, direction):
        return Cube(self.x + direction[0], self.y + direction[1], self.z + direction[2])

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)

    def __sub__(self, other):
        result = self.x - other.x, self.y - other.y, self.z - other.z
        maximum = max(result)
        assert min(result) == 0 and sum(x == 0 for x in result) == 2
        direction = [
            tuple((x // maximum) * (y + 1) for x in result) for y in range(maximum - 1)
        ]
        return [other.move(x) for x in direction]


@dataclass
class Brick:
    brick_id: int
    start: Cube
    end: Cube

    @classmethod
    def from_line(cls, brick_id, line):
        data = (tuple(map(int, x.split(","))) for x in line.split("~"))
        return cls(brick_id, start=Cube(*next(data)), end=Cube(*next(data)))

    @property
    def locations(self):
        if self.start == self.end:
            return ((self.start.x, self.start.y),)
        return tuple(
            (cube.x, cube.y)
            for cube in [self.start, *(self.end - self.start), self.end]
        )

    def __len__(self):
        return (
            max(
                self.end.x - self.start.x,
                self.end.y - self.start.y,
                self.end.z - self.start.z,
            )
            + 1
        )

    def __eq__(self, other):
        return (self.start == other.start) and (self.end == other.end)

    def __lt__(self, other):
        return self.end.z < other.end.z

    def is_vertical(self):
        return self.start.z != self.end.z


def layout_bricks(bricks, exclude=None):
    bricks = [brick for brick in bricks if brick.brick_id != exclude]
    max_r = max(max(brick.start.y, brick.end.y) for brick in bricks)
    max_c = max(max(brick.start.x, brick.end.x) for brick in bricks)
    elev = np.zeros((max_r + 1, max_c + 1), dtype=int)

    for b in bricks:
        if b.is_vertical():
            height = b.end.z - b.start.z
            previous_elev = elev[max_r - b.end.y, b.end.x]
            elev[max_r - b.end.y, b.end.x] = b.end.z = previous_elev + height + 1
            b.start.z = b.end.z - height
        else:
            max_elev_in_loc = max(elev[max_r - y, x] for x, y in b.locations)
            for x, y in b.locations:
                b.start.z = b.end.z = elev[max_r - y, x] = max_elev_in_loc + 1

    return sorted(bricks)


def identify_brick_rel(bricks):
    brick_locations = {}
    _brick_under_elev = {}

    for b in bricks:
        brick_locations[b.brick_id] = b.locations
        _brick_under_elev[b.brick_id] = b.start.z - 1

    brick_supported_by_brick = {}
    brick_supports_brick = {}
    for brick_id, loc, under_elev in zip(
        brick_locations.keys(), brick_locations.values(), _brick_under_elev.values()
    ):
        brick_supported_by_brick[brick_id] = set()
        brick_supports_brick[brick_id] = set()
        for b in bricks:
            if b.brick_id == brick_id:
                continue
            if under_elev == b.end.z and set(loc) & set(b.locations):
                brick_supported_by_brick[brick_id].add(b.brick_id)
                brick_supports_brick[b.brick_id].add(brick_id)

    return _brick_under_elev, brick_supports_brick, brick_supported_by_brick


if __name__ == "__main__":
    with open("day_22/input.txt") as f:
        lines = [x.strip("\n") for x in f.readlines()]

    brick_group = sorted([Brick.from_line(i, line) for i, line in enumerate(lines)])

    (brick_under_elev, supports_brick, supported_by_brick) = identify_brick_rel(
        layout_bricks(brick_group)
    )

    # PART 1
    count = 0
    brick_unsafe = []
    for brick, supported_bricks in supports_brick.items():
        for supported_brick in supported_bricks:
            if len(supported_by_brick[supported_brick]) == 1:
                break
        else:
            count += 1
            continue
        brick_unsafe.append(brick)
    print(f"PART 1: {count}")

    # PART 2
    count = 0
    for brick in tqdm(brick_unsafe):
        _brick_under_elev, *_ = identify_brick_rel(
            layout_bricks(brick_group, exclude=brick)
        )
        count += sum(brick_under_elev.get(k) != v for k, v in _brick_under_elev.items())
    print(f"PART 2: {count}")
