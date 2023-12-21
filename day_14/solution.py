from itertools import pairwise, product

import numpy as np


def calculate_load(array):
    lines = [array[r, :] for r in range(array.shape[0])]
    total = 0
    for row, line in enumerate(lines, start=1):
        total += (array.shape[0] - row) * (line == "O").sum()
    return total


def tilt_up(lines):
    new_lines = []
    for line in lines:
        new_line = []
        for left, right in pairwise(np.where(line == "#")[0]):
            if left == 0:
                new_line.append("#")
            for rounded in np.where(line == "O")[0]:
                if rounded < left:
                    continue
                if left < rounded < right:
                    new_line.append("O")
                    continue
                if rounded > right:
                    break
            for dotted in np.where(line == ".")[0]:
                if dotted < left:
                    continue
                if left < dotted < right:
                    new_line.append(".")
                    continue
                if dotted > right:
                    break
            new_line.append("#")
        new_lines.append(new_line)
    return new_lines


def cycle_n(array, n=1, m=1, rotate=True):
    for _ in product(range(n), range(m)):
        lines = [array[:, c] for c in range(array.shape[1])]
        array = np.array(tilt_up(lines)).T
        if rotate:
            array = np.rot90(array, -1)
    return array


if __name__ == "__main__":
    with open("day_14/input.txt") as f:
        _data = np.array([list(x) for x in f.read().split()])

    # Enclose array with "#"
    data = np.roll(
        np.insert(np.insert(_data, 0, values="#", axis=0), 0, values="#", axis=0),
        shift=-1,
        axis=0,
    )
    data = np.roll(
        np.insert(np.insert(data, 0, values="#", axis=1), 0, values="#", axis=1),
        shift=-1,
        axis=1,
    )

    print(f"PART 1: {calculate_load(cycle_n(data, n=1, m=1, rotate=False))}")

    # Collect all results after each cycle until the pattern repeats
    results = []
    for i in range(1_000_000_000):
        data = cycle_n(data, n=4, m=1, rotate=True)
        for first_occurence, result in enumerate(results):
            if np.array_equal(data, result):
                break
        else:
            results.append(data)
            continue
        break

    wavelength_excess = (1_000_000_000 - first_occurence) % (i - first_occurence)

    data = cycle_n(data, n=4, m=wavelength_excess - 1, rotate=True)
    print(f"PART 2: {calculate_load(data)}")
