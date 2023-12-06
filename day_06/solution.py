import math
import re

PART = 2


def counter(b, c):
    a = -1
    determinant = b**2 - 4 * a * c
    assert determinant > 0
    sol_1 = math.ceil((-b - math.sqrt(determinant)) / 2 / a)
    sol_2 = math.ceil((-b + math.sqrt(determinant)) / 2 / a)
    return sol_1 - sol_2


if __name__ == "__main__":
    with open("day_06/input.txt") as f:
        data = f.read().strip("\n").split("\n")
        if PART == 1:
            times, distances = [
                [int(y) for y in re.findall(r"\d+", x.split(":")[1])] for x in data
            ]
        elif PART == 2:
            times, distances = [[int(x.split(":")[1].replace(" ", ""))] for x in data]

    win_product = 1
    for t, d in zip(times, distances):
        # To win, speed * (time - speed) > distance
        # -speed**2 + time(speed) - distance = 0
        # -2x**2 + tx - d = 0; a = -1, b = t, c = -d
        win_product *= counter(t, -d)
    print(win_product)
