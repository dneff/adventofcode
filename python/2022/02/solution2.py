
def printSolution(x):
    print(f"The solution is: {x}")

gestures = {
    "A": "ROCK",
    "B": "PAPER",
    "C": "SCISSORS",
    "X": "ROCK",
    "Y": "PAPER",
    "Z": "SCISSORS",

}

values = {
    "ROCK": 1,
    "PAPER": 2,
    "SCISSORS": 3
}

def scoreBattle(them, us):
    them = values[gestures[them]]
    if us == "X":
        score = them - 1
        if score == 0:
            score = 3
        return score
    elif us == "Y":
        return 3 + them
    elif us == "Z":
        score = them + 1
        if score == 4:
            score = 1
        return 6 + score


def main():
    file = open('../input/02.txt', 'r', encoding='utf-8')
    result = 0
    for line in file.readlines():
        them, us = [x for x in line.strip().split(' ')]
        result += scoreBattle(them, us)

    printSolution(result)

if __name__ == "__main__":
    main()
