import numpy as np

if __name__ == "__main__":  # noqa C901
    with open("day_13/input.txt") as f:
        _patterns = []
        for x in f.read().split("\n\n"):
            pattern = []
            for y in x.split():
                pattern.append(list(y))
            _patterns.append(pattern)

    patterns = [np.array(pattern) for pattern in _patterns]

    PART_1 = 0
    for pattern in patterns:
        rows, cols = pattern.shape
        for r in range(rows - 1):
            offset = subtotal = 0
            while np.array_equal(pattern[r - offset, :], pattern[r + 1 + offset, :]):
                if r - offset == 0 or r + 1 + offset == rows - 1:
                    subtotal += (r + 1) * 100
                    break
                offset += 1
            if subtotal > 0:
                break
        else:
            for c in range(cols - 1):
                offset = subtotal = 0
                while np.array_equal(
                    pattern[:, c - offset], pattern[:, c + 1 + offset]
                ):
                    if c - offset == 0 or c + 1 + offset == cols - 1:
                        subtotal += c + 1
                        break
                    offset += 1
                if subtotal > 0:
                    break
        PART_1 += subtotal

    PART_2 = 0
    for pattern in patterns:
        rows, cols = pattern.shape
        for r in range(rows - 1):
            smudge = False
            offset = subtotal = 0
            while (r - offset >= 0 and r + 1 + offset <= rows - 1) and (
                diff := np.sum((pattern[r - offset, :] != pattern[r + 1 + offset, :]))
            ) <= 1:
                if diff == 1:
                    if smudge:
                        break
                    smudge = True
                if (r - offset == 0 or r + 1 + offset == rows - 1) and smudge:
                    subtotal += (r + 1) * 100
                    break
                offset += 1
            if subtotal > 0 and smudge:
                break
        else:
            for c in range(cols - 1):
                smudge = False
                offset = subtotal = 0
                while (c - offset >= 0 and c + 1 + offset <= cols - 1) and (
                    diff := np.sum(
                        (pattern[:, c - offset] != pattern[:, c + 1 + offset])
                    )
                ) <= 1:
                    if diff == 1:
                        if smudge:
                            break
                        smudge = True
                    if (c - offset == 0 or c + 1 + offset == cols - 1) and smudge:
                        subtotal += c + 1
                        break
                    offset += 1
                if subtotal > 0 and smudge:
                    break
        PART_2 += subtotal

    print(f"{PART_1 = }")
    print(f"{PART_2 = }")
