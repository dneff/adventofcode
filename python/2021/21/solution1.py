
def printSolution(x):
    print(f"The solution is {x}")


def deterministic_die():
    dice_face = 1
    while True:
        yield dice_face
        dice_face = (dice_face + 1) % 101
        if dice_face == 0:
            dice_face += 1


def next_position(position, x):
    position = (position + x) % 10
    if position == 0:
        position = 10
    return position


def main():
    puzzle = [4, 9]
    test = [4, 8]

    positions = puzzle

    scores = [0, 0]
    
    play_die = deterministic_die()
    turn = 0
    rolls = 0
    while max(scores) < 1000:
        print(scores)
        moves = sum([next(play_die), next(play_die), next(play_die)])
        rolls += 3
        positions[turn] = next_position(positions[turn], moves)
        scores[turn] += positions[turn]
        
        turn = (turn + 1) % 2
    
    printSolution(min(scores) * rolls)


if __name__ == "__main__":
    main()