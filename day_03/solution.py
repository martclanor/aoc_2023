import re
from dataclasses import dataclass


@dataclass
class Line:
    data: str

    def match(self, regex):
        for m in re.compile(regex).finditer(self.data):
            yield m.group(), m.start(), m.end()

    def expanded_match(self, regex):
        for char, start, end in self.match(regex):
            if start != 0:
                start -= 1
            if end != len(self.data):
                end += 1
            yield char, start, end


@dataclass
class Triplet:
    mid: Line
    sides: list[Line]

    @property
    def lines(self):
        return [self.mid] + self.sides

    def get_subtotal(self, part):
        subtotal = 0
        if part == 1:
            for number, start, end in self.mid.expanded_match(r"\d+"):
                for line in self.lines:
                    substring = line.data[start:end]
                    if re.search(r"[^.0-9]", substring) is not None:
                        subtotal += int(number)
                        break
        if part == 2:
            for _, start, end in self.mid.expanded_match(r"[*]"):
                number_pair = []
                for line in self.lines:
                    for number, num_start, num_end in line.match(r"\d+"):
                        if min(num_end, end) > max(num_start, start):
                            number_pair.append(int(number))
                if len(number_pair) == 2:
                    subtotal += number_pair[0] * number_pair[1]
        return subtotal


if __name__ == "__main__":
    with open("day_03/input.txt") as f:
        data = f.read().splitlines()

    PART_1_TOTAL = 0
    PART_2_TOTAL = 0
    for i, j in enumerate(data):
        if i == 0:
            triplet = Triplet(mid=Line(j), sides=[Line(data[i + 1])])
        elif i == len(data) - 1:
            triplet = Triplet(mid=Line(j), sides=[Line(data[i - 1])])
        else:
            triplet = Triplet(mid=Line(j), sides=[Line(data[i + 1]), Line(data[i - 1])])

        PART_1_TOTAL += triplet.get_subtotal(part=1)
        PART_2_TOTAL += triplet.get_subtotal(part=2)

    print(f"{PART_1_TOTAL = }")
    print(f"{PART_2_TOTAL = }")
