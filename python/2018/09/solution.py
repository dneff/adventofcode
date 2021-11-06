from collections import deque, defaultdict

def printSolution(x):
    print(f"The solution is {x}")

def place_marble(circle, marble_value):
    score  = 0
    if marble_value % 23 == 0:
        score += marble_value
        move = 7
        circle.rotate(move)
        score += circle.popleft()
    else:
        move = -2
        circle.rotate(move)
        circle.appendleft(marble_value)
    return score


def main():
    test = {
        'players': 30,
        'max_value': 5807
    }

    puzzle1 = {
        'players': 463,
        'max_value': 71787
    }

    puzzle2 = {
        'players': 463,
        'max_value': 71787 * 100
    }
    active = puzzle2

    circle = deque()
    scores = defaultdict(int)
    
    marble_value = 0
    circle.appendleft(marble_value)
    marble_value += 1

    while marble_value <= active['max_value']:
        player = marble_value % active['players']
        scores[player] += place_marble(circle, marble_value)
        marble_value += 1

    printSolution(max(scores.values()))


if __name__ == "__main__":
    main()