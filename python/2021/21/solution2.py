
from collections import defaultdict
import functools

def printSolution(x):
    print(f"The solution is {x}")


dirac_rolls = []
for a in range(1, 4):
    for b in range(1, 4):
        for c in range(1, 4):
            dirac_rolls.append(a+b+c)


@functools.lru_cache(maxsize=None)
def turn(pos0, score0, pos1, score1, player_turn):
    if score0 >= 21:
        return [1, 0]

    if score1 >= 21:
        return [0, 1]
    
    win0, win1 = 0, 0
    
    for roll in dirac_rolls:
        next_turn = (player_turn + 1) % 2
        new_move = [pos0, score0, pos1, score1, next_turn]
        new_move[player_turn * 2] = (new_move[player_turn * 2] + roll) % 10
        if new_move[player_turn * 2] == 0:
            new_move[player_turn * 2] = 10
        new_move[player_turn * 2 + 1] = new_move[player_turn * 2 + 1] + new_move[player_turn*2]
        w0, w1 = turn(*new_move)
        
        win0 += w0
        win1 += w1
    
    return [win0, win1]
    
    
def main():
    puzzle = [4, 9]
    test = [4, 8]

    positions = puzzle

    # p0 position, p0 score, p1 position, p1 score, players_turn
    starting = (positions[0], 0, positions[1], 0, 0)

    wins = turn(*starting)

    print(wins)
    printSolution(max(wins))


if __name__ == "__main__":
    main()
