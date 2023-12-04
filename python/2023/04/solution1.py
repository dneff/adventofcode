
def print_solution(x):
    """prints solution"""
    print(f"The solution is: {x}")


def main():
    """solves day 4 part 1"""
    filename = "./python/2023/input/04.txt"
    cards = {}
    with open(filename, "r", encoding="utf-8") as file:
        for idx, line in enumerate(file.readlines()):
            winners, numbers = line.strip().split(':')[1].split(' | ')
            winners = [int(x) for x in winners.split()]
            numbers = [int(x) for x in numbers.split()]
            cards[idx+1] = {'winners':winners[:], 'numbers': numbers[:]}

    score = 0
    # check for winners in each card
    # score = 2^(matches)
    for _, card in cards.items():
        matches = set(card['winners']) & set(card['numbers'])
        if len(matches) > 0:
            score += 2 ** (len(matches) - 1)

    print_solution(score)


if __name__ == "__main__":
    main()