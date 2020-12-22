from collections import defaultdict


class Combat:
    def __init__(self):
        self.round = 0
        self.score = 0
        self.winner = None
        self.players = []
        self.history = []

    def play(self):
        p1, p2 = self.players[0], self.players[1]

        if self.winner:
            return self.winner

        if len(p1) == 0 or len(p2) == 0:
            if len(p1):
                self.winner = 1
            else:
                self.winner = 2
            self.findScore()
            return self.winner

        # check history
        hand1, hand2 = hash(tuple(p1)), hash(tuple(p2))
        if (hand1 in self.history[0]) or (hand2 in self.history[1]):
            self.winner = 1
            return self.winner
        else:
            self.history[0].add(hand1)
            self.history[1].add(hand2)

        self.round += 1
        card1, card2 = p1.pop(0), p2.pop(0)

        # check for subgame
        if len(p1) >= card1 and len(p2) >= card2:
            subgame = Combat()
            subgame.addPlayer(p1[:card1])
            subgame.addPlayer(p2[:card2])
            winner = subgame.resolveGame()
            if winner == 1:
                p1.extend([card1, card2])
            else:
                p2.extend([card2, card1])

        elif card1 > card2:
            p1.extend([max(card1, card2), min(card1, card2)])
        else:
            p2.extend([max(card1, card2), min(card1, card2)])

    def findScore(self):
        for idx, p in enumerate(self.players):
            if len(p):
                self.winner = idx + 1
                card_scores = [x * y for x, y in zip(p, range(len(p), -1, -1))]
                self.score = sum(card_scores)
                return self.score

    def addPlayer(self, data):
        self.players.append([])
        self.players[-1].extend(data)
        self.history.append(set())

    def resolveGame(self):
        while not self.winner:
            self.play()
        return self.winner

    def __repr__(self):
        return f"Combat: round: {self.round}, players: {self.players}, score: {self.score}, winner: {self.winner}"


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

    game.resolveGame()

    printSolution(game.score)


if __name__ == "__main__":
    main()
