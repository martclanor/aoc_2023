import math
import re
from itertools import cycle

PART = 2

if __name__ == "__main__":
    with open("day_08/input.txt") as f:
        _directions, _nodes = f.read().split("\n\n")
    directions = list(map(int, _directions.replace("L", "0").replace("R", "1")))
    nodes = {
        k: (v1, v2)
        for k, v1, v2 in [re.findall("[A-Z]+", x) for x in _nodes.strip().split("\n")]
    }

    if PART == 1:
        starts = ["AAA"]
        final = "ZZZ"
    elif PART == 2:
        starts = [x for x in nodes.keys() if x.endswith("A")]
        final = "Z"

    wavelengths = []
    for start in starts:
        i = 0
        direction_loop = cycle(directions)
        while True:
            i += 1
            start = nodes[start][next(direction_loop)]
            if start.endswith(final):
                wavelengths.append(i)
                break
    print(math.lcm(*wavelengths))
