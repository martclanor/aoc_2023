from heapq import heappop, heappush

import numpy as np

OFFSETS = {
    # turn: {current_direction: (delta_row, delta_col)}
    "straight": {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)},
    "left": {"up": (0, -1), "down": (0, 1), "left": (1, 0), "right": (-1, 0)},
    "right": {"up": (0, 1), "down": (0, -1), "left": (-1, 0), "right": (1, 0)},
}
DIRECTION_LABEL = {
    (-1, 0): "up",
    (1, 0): "down",
    (0, -1): "left",
    (0, 1): "right",
}


def dijkstra(grid, min_steps, max_steps):
    rows, cols = grid.shape

    # Start at the upper left corner, considering the two possible directions
    priority_queue = [
        (0, (0, 0), "right", 0),
        (0, (0, 0), "down", 0),
    ]  # Heatloss, location, direction, number of steps on the direction

    # Collect visited nodes to avoid duplicate evaluation
    visited_nodes = set()  # location, direction, number of steps on the direction

    def within_grid(loc):
        return 0 <= loc[0] < rows and 0 <= loc[1] < cols

    def get_neighbor(loc, direction):
        return loc[0] + direction[0], loc[1] + direction[1]

    while priority_queue:
        # Pop the current node with the lowest heatloss
        heatloss, location, direction, steps = heappop(priority_queue)

        if location == (rows - 1, cols - 1):
            return heatloss

        if (location, direction, steps) in visited_nodes:
            continue
        visited_nodes.add((location, direction, steps))

        if steps < max_steps:
            if within_grid(
                (neighbor := get_neighbor(location, OFFSETS["straight"][direction]))
            ):
                heappush(
                    priority_queue,
                    (
                        heatloss + grid[neighbor],
                        neighbor,
                        direction,
                        steps + 1,
                    ),
                )

        if steps >= min_steps:
            for turn in ["left", "right"]:
                if within_grid(
                    (neighbor := get_neighbor(location, OFFSETS[turn][direction]))
                ):
                    heappush(
                        priority_queue,
                        (
                            heatloss + grid[neighbor],
                            neighbor,
                            DIRECTION_LABEL[OFFSETS[turn][direction]],
                            1,
                        ),
                    )


if __name__ == "__main__":
    with open("day_17/input.txt") as file:
        data = np.array([list(map(int, x)) for x in file.read().split()])
    print(f"PART 1: {dijkstra(data, min_steps=0, max_steps=3)}")
    print(f"PART 2: {dijkstra(data, min_steps=4, max_steps=10)}")
