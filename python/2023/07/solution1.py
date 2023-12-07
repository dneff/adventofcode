"""solves 2023 day 7 problem 1"""
from collections import defaultdict

order = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]


def print_solution(x):
    """prints formatted solution"""
    print(f"The solution is: {x}")


class Hand:
    """hand of cards"""

    def __init__(self, cards, bid, order):
        self.order = order
        self.hand = defaultdict(int)
        self.cards = []
        self.bid = bid
        self.strength = 0

        self.cards[:] = cards
        for card in self.cards:
            self.hand[card] += 1

        self.resolve_strength()

    def resolve_strength(self):
        """find hand strength"""
        counts = list(self.hand.values())

        if max(counts) == 5:
            self.strength = 7
        elif max(counts) == 4:
            self.strength = 6
        elif max(counts) == 3:
            if counts.count(2):
                self.strength = 5
            else:
                self.strength = 4
        elif max(counts) == 2:
            if counts.count(2) == 2:
                self.strength = 3
            else:
                self.strength = 2
        elif max(counts) == 1:
            self.strength = 1

    def __lt__(self, other):
        """make hands sortable"""
        if self.strength != other.strength:
            return self.strength < other.strength
        for s, o in zip(self.cards, other.cards):
            if s == o:
                continue
            else:
                return self.order.index(s) < self.order.index(o)


def main():
    """finds solution"""
    hands = []
    filename = "./python/2023/input/07.txt"
    with open(filename, "r", encoding="utf-8") as f:
        for line in f.readlines():
            hand, bid = line.strip().split()
            bid = int(bid)
            h = Hand(hand, bid, order)
            hands.append(h)

    hands.sort()

    winnings = 0
    for idx, hand in enumerate(hands):
        score = (idx + 1) * hand.bid
        winnings += score

    print_solution(winnings)


if __name__ == "__main__":
    main()
