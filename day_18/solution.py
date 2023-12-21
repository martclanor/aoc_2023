from skspatial.measurement import area_signed

PART = 2
if __name__ == "__main__":
    hex_direction_map = {0: "R", 1: "D", 2: "L", 3: "U"}
    with open("day_18/input.txt") as f:
        digs = [
            (
                y[0],  # PART 1 direction
                int(y[1]),  # PART 1 count
                hex_direction_map[int(y[2][-2:-1])],  # PART 2 direction
                int(y[2][2:7], 16),  # PART 2 count
            )
            for y in [x.split() for x in f.readlines()]
        ]

    direction_map = {
        "U": (-1, 0),
        "D": (1, 0),
        "L": (0, -1),
        "R": (0, 1),
    }

    dig_path = []

    if PART == 1:
        for direction, count, *_ in digs:
            dig_path.append(tuple(x * count for x in direction_map[direction]))
    elif PART == 2:
        for *_, direction, count in digs:
            dig_path.append(tuple(x * count for x in direction_map[direction]))

    current = (0, 0)
    dig_loc = []
    for dr, dc in dig_path:
        current = current[0] + dr, current[1] + dc
        dig_loc.append(current)

    perimeter = sum(abs(x[0]) + abs(x[1]) for x in dig_path)

    # To avoid integer overflow while using area_signed, scale down the distances
    factor = 1_000_000
    dig_loc = [(x[0] / factor, x[1] / factor) for x in dig_loc]
    print(int(abs(area_signed(dig_loc)) * factor**2 + 1 + perimeter / 2))
