import re

PART = 2

converter = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

numbers = []
with open("day_01/input.txt") as f:
    for line in f.readlines():
        digits = []
        for i, _ in enumerate(line):
            if PART == 2:
                for j, k in converter.items():
                    if (m := re.match(j, line[i:])) is not None:
                        digits.append(k)
                        break

            first_char = line[i : i + 1]
            if first_char.isdigit():
                digits.append(first_char)
        numbers.append(int("".join([digits[0], digits[-1]])))

print(sum(numbers))
