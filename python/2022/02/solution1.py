
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
    score = 0
    if us == them:
        score = 3
    elif (us == "ROCK" and them == "SCISSORS") \
        or (us == "PAPER" and them == "ROCK") \
        or (us == "SCISSORS" and them == "PAPER"):
        score = 6
    return score + values[us]



def main():
    file = open('../input/02.txt', 'r', encoding='utf-8')
    result = 0
    for line in file.readlines():
        them, us = [gestures[x] for x in line.strip().split(' ')]
        result += scoreBattle(them, us)

    printSolution(result)

if __name__ == "__main__":
    main()
