import re
from dataclasses import dataclass, field


@dataclass
class Lens:
    string: str

    def __post_init__(self):
        self.match = re.search(
            r"(?P<label>[a-z]+)(?P<operation>[-=])(?P<focal_length>[\d]?)", self.string
        )

    def __eq__(self, other):
        if self.label == other.label:
            return True
        return False

    @property
    def label(self):
        return self.match.group("label")

    @property
    def operation(self):
        return self.match.group("operation")

    @property
    def focal_length(self):
        return int(self.match.group("focal_length"))

    @staticmethod
    def convert(sequence):
        value = 0
        for c in sequence:
            value = ((value + ord(c)) * 17) % 256
        return value


@dataclass
class Box:
    index: int
    slots: list = field(default_factory=list)


if __name__ == "__main__":
    with open("day_15/input.txt") as f:
        data = f.read().strip("\n")
    lenses = [Lens(x) for x in data.split(",")]
    boxes = [Box(x + 1) for x in range(256)]

    for lens in lenses:
        box_slots = boxes[Lens.convert(lens.label)].slots
        if lens.operation == "=":
            if lens in box_slots:
                box_slots[box_slots.index(lens)] = lens
            else:
                box_slots.append(lens)
        elif lens.operation == "-":
            if lens in box_slots:
                box_slots.remove(lens)

    PART_2 = 0
    for box in boxes:
        if not box.slots:
            continue
        for i, lens in enumerate(box.slots, start=1):
            PART_2 += box.index * i * lens.focal_length

    print(f"PART_1 = {sum(Lens.convert(lens.string) for lens in lenses)}")
    print(f"{PART_2 = } ")
