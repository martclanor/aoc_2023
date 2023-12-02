from dataclasses import dataclass

MAX_RED = 12
MAX_GREEN = 13
MAX_BLUE = 14


@dataclass
class CubeSubset:
    red: int = 0
    green: int = 0
    blue: int = 0


@dataclass
class CubeSubsetGroup:
    data: list[CubeSubset]

    @property
    def max_red(self):
        return max(cube_subset.red for cube_subset in self.data)

    @property
    def max_green(self):
        return max(cube_subset.green for cube_subset in self.data)

    @property
    def max_blue(self):
        return max(cube_subset.blue for cube_subset in self.data)

    def power(self):
        return self.max_red * self.max_green * self.max_blue


@dataclass
class Game:
    record: str

    @property
    def game_id(self):
        return int(self.record.partition(":")[0].partition(" ")[-1])

    @property
    def game_data(self):
        return self.record.partition(":")[-1].split(";")

    def get_cube_subsets(self):
        # return list of cube subsets
        cube_subsets = []
        for i in self.game_data:
            cube_subsets_data = {}
            for j in i.split(","):
                count, color = j.strip(" ").split(" ")
                cube_subsets_data[color] = int(count)
            cube_subsets.append(CubeSubset(**cube_subsets_data))
        return cube_subsets


if __name__ == "__main__":
    games = []
    with open("day_02/input.txt") as f:
        for line in f.read().splitlines():
            games.append(Game(line))

    # PART 1
    possible_games = []
    for game in games:
        for cube_subset in game.get_cube_subsets():
            if (
                (cube_subset.red <= MAX_RED)
                and (cube_subset.green <= MAX_GREEN)
                and (cube_subset.blue <= MAX_BLUE)
            ):
                continue
            break
        else:
            possible_games.append(game.game_id)

    print(sum(possible_games))

    # PART 2
    power_of_games = []
    for game in games:
        power_of_games.append(CubeSubsetGroup(game.get_cube_subsets()).power())

    print(sum(power_of_games))
