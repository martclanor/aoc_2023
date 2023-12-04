import re

with open("day_04/input.txt") as f:
    data = [x.split(":")[1] for x in f.read().splitlines()]

PART_1 = 0
card_counter = [1] * len(data)

for i, j in enumerate(data):
    winning, mine = (set(re.findall(r"\d+", x)) for x in j.split("|"))
    if (match_count := len(winning.intersection(mine))) > 0:
        PART_1 += 2 ** (match_count - 1)
        card_counter[i + 1 : i + 1 + match_count] = [
            (x + card_counter[i]) for x in card_counter[i + 1 : i + 1 + match_count]
        ]

print(f"{PART_1 = }")
print(f"PART_2 = {sum(card_counter)}")
