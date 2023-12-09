import numpy as np


def subtract_recursively(group):
    while len(group) > 1:
        diff = group[-2] - group[-1]
        group = group[:-2]
        group.append(diff)
    return diff


if __name__ == "__main__":
    with open("day_09/input.txt") as f:
        hists = (np.array(list(map(int, x.split()))) for x in f.read().splitlines())

    part_1 = 0
    part_2 = 0
    for hist in hists:
        starts = [hist[0]]
        while any(hist):
            part_1 += hist[-1]
            hist = np.diff(hist)
            starts.append(hist[0])
        part_2 += subtract_recursively(starts)
    print(f"{part_1 = }")
    print(f"{part_2 = }")
