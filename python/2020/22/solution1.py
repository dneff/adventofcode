from collections import deque, defaultdict


class Combat:
    def __init__(self):
        self.round = 0
        self.score = 0
        self.players = []

    def play(self):
        p1, p2 = self.players[0], self.players[1]
        if len(p1) == 0 or len(p2) == 0:
            return self.findScore()
        self.round += 1
        card1, card2 = p1.popleft(), p2.popleft()
        if card1 > card2:
            p1.extend([max(card1, card2), min(card1, card2)])
        else:
            p2.extend([max(card1, card2), min(card1, card2)])

    def findScore(self):
        for p in self.players:
            if len(p):
                card_scores = [x * y for x, y in zip(p, range(len(p), -1, -1))]
                self.score = sum(card_scores)
                return self.score

    def addPlayer(self, data):
        self.players.append(deque())
        self.players[-1].extend(data)

    def __repr__(self):
        return f"Combat: round: {self.round}, players: {self.players}"


def printSolution(x):
    print(f"The solution is: {x}")


def main():
    file = open("input.txt", "r")

    player_data = defaultdict(list)
    player_id = 0

    for line in file:
        l = line.strip()

        if not l:
            player_id += 1
        elif "Player" in l:
            continue
        else:
            player_data[player_id].append(int(l))

    game = Combat()

    for cards in player_data.values():
        game.addPlayer(cards)

    while game.score == 0:
        game.play()

    printSolution(game.score)


if __name__ == "__main__":
    main()
