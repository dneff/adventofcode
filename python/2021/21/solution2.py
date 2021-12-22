
from collections import defaultdict


def printSolution(x):
    print(f"The solution is {x}")


def next_position(position, x):
    position = (position + x) % 10
    if position == 0:
        position = 10
    return position


def main():
    puzzle = [4, 9]
    test = [4, 8]

    positions = test

    turn = 0
    games = defaultdict(int)

    # p0 position, p1 position, p0 score, p1 score, players_turn
    starting = (positions[0], positions[1], 0, 0, turn)

    games[starting] += 1

    roll_distribution = defaultdict(int)
    for a in range(1, 4):
        for b in range(1, 4):
            for c in range(1, 4):
                roll_distribution[a+b+c] += 1

    wins = [0, 0]

    while len(games.keys()) != 0:
        k, count = games.popitem()
        if max(k) > 10:
            print(len(games.keys()), k, max(k), wins)
        if max(k) >= 21:
            if k[2] >= 21:
                wins[0] += count
            else:
                wins[1] += count
            continue

        turn, p0, p1, score0, score1 = k

        new_turn = (turn + 1) % 2
        if turn == 0:
            for moves, counts in roll_distribution.items():
                new_pos = next_position(p0, moves)
                new_state = (new_pos, p1, score0 + new_pos, score1, new_turn)
                games[new_state] += count
        else:
            for moves, counts in roll_distribution.items():
                new_pos = next_position(p1, moves)
                new_state = (p0, new_pos, score0, score1 + new_pos, new_turn)
                games[new_state] += count

    printSolution(max(wins))


if __name__ == "__main__":
    main()
