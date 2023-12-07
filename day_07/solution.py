from collections import Counter
from dataclasses import dataclass
from itertools import chain

JOKER = False  # for Part 1, False; for Part 2, True


@dataclass
class Hand:
    card: str
    bid: int
    joker: bool = False

    def __post_init__(self):
        self.orig_card = self.card
        self.most_common, self.nunique = self.get_stats()

        if self.joker:
            if self.most_common[0][0] == "J" and self.nunique > 1:
                self.card = self.card.replace("J", self.most_common[1][0])
            else:
                self.card = self.card.replace("J", self.most_common[0][0])
            self.most_common, self.nunique = self.get_stats()

    def get_stats(self):
        most_common = Counter(self.card).most_common()
        return most_common, len(most_common)

    @staticmethod
    def get_sorting(joker):
        if not joker:
            return "23456789TJQKA"
        return "J23456789TQKA"


if __name__ == "__main__":
    with open("day_07/input.txt") as f:
        hands = [
            Hand(c, int(b), joker=JOKER)
            for c, b in (x.split() for x in f.read().splitlines())
        ]

    high_card = []
    one_pair = []
    two_pair = []
    three_of_a_kind = []
    full_house = []
    four_of_a_kind = []
    five_of_a_kind = []

    for hand in hands:
        match hand.nunique:
            case 5:
                # count: 1, 1, 1, 1, 1
                high_card.append(hand)
            case 4:
                # count: 2, 1, 1, 1
                one_pair.append(hand)
            case 3:
                if hand.most_common[0][1] == 2:
                    # count: 2, 2, 1
                    two_pair.append(hand)
                else:
                    # count: 3, 1, 1
                    three_of_a_kind.append(hand)
            case 2:
                if hand.most_common[0][1] == 3:
                    # count: 3, 2
                    full_house.append(hand)
                else:
                    # count: 4, 1
                    four_of_a_kind.append(hand)
            case 1:
                # count: 5
                five_of_a_kind.append(hand)

    hands_grouped = [
        high_card,
        one_pair,
        two_pair,
        three_of_a_kind,
        full_house,
        four_of_a_kind,
        five_of_a_kind,
    ]

    for group in hands_grouped:
        group[:] = sorted(
            group,
            key=lambda hand: [Hand.get_sorting(JOKER).index(c) for c in hand.orig_card],
        )

    TOTAL = 0
    for i, hand in enumerate(chain(*hands_grouped), start=1):
        TOTAL += i * hand.bid
    print(f"{TOTAL = }")
