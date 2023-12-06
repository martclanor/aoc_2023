import re
from dataclasses import dataclass
from functools import cached_property
from itertools import chain

PART = 2


@dataclass
class Range:
    data: str

    def __post_init__(self):
        self.dest, self.start, self.count = [int(x) for x in self.data.split(" ")]

    @property
    def offset(self):
        return self.dest - self.start

    @property
    def end(self):
        return self.start + self.count - 1


@dataclass
class Mapper:
    line: str

    def __post_init__(self):
        self.data = self.line.split(":")[1].strip("\n")

    @cached_property
    def ranges(self):
        return [Range(x) for x in self.data.split("\n")]

    def convert(self, number):
        for range_ in self.ranges:
            if range_.start <= number <= range_.end:
                return number + range_.offset
        return number


@dataclass
class SeedRange:
    data: str

    @property
    def start(self):
        return int(self.data.split()[0])

    @property
    def end(self):
        return int(self.data.split()[1]) + self.start

    def expand(self):
        return range(self.start, self.end)


if __name__ == "__main__":
    with open("day_05/input.txt") as f:
        raw_data = f.read().split("\n\n")
    if PART == 1:
        seeds = [int(x) for x in re.findall(r"\d+", raw_data[0])]
    elif PART == 2:
        seeds = chain(
            SeedRange(line).expand() for line in re.findall(r"[\d]+ [\d]+", raw_data[0])
        )

    mappers = [Mapper(line) for line in raw_data[1:]]
    min_location = None

    for seed in seeds:
        mapping = seed
        for mapper in mappers:
            mapping = mapper.convert(mapping)
        if min_location is None:
            min_location = mapping
        else:
            min_location = min(min_location, mapping)
    print(f"{min_location = }")
