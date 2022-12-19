from collections import defaultdict
import copy
from os import remove

def printSolution(x):
    print(f"The solution is {x}")

def rotate_card(data):
    return [[data[j][i] for j in range(len(data))] for i in range(len(data[0])-1,-1,-1)]

class BingoCard():
    def __init__(self, card_lines):
        self.card_lines = card_lines
        self.called = []

    def checkNumber(self, x):
        result = 0

        for line in self.card_lines:
            try:
                line.remove(x)
            except ValueError:
                continue
            if len(line) == 0:
                remaining_numbers = []
                list(remaining_numbers.extend(x) for x in self.card_lines[:5])
                remaining_numbers = set(remaining_numbers)
                result = sum(list(remaining_numbers)) * x
                break

        return result

    def __repr__(self) -> str:
        return f"BingoCard: {self.card_lines}"

def main():
    puzzle = 'input.txt'
    test = 'test.txt'
    file = open(puzzle, 'r')
    bingo_calls = [int(x) for x in file.readline().strip().split(",")]
    file.readline()

    bingo_cards = []

    card_data = []
    for line in file.readlines():
        if line.strip():
            card_data.append([int(x) for x in line.strip().split()])
        else:
            card_data.extend(rotate_card(card_data))
            x = BingoCard(copy.deepcopy(card_data))
            bingo_cards.append(x)
            card_data.clear()

    card_data.extend(rotate_card(card_data))
    x = BingoCard(copy.deepcopy(card_data))
    bingo_cards.append(x)
    card_data.clear()

    cards_to_purge = []
    for number in bingo_calls:
        if len(bingo_cards) == 1:
            break

        for card_index, card in enumerate(bingo_cards):
            card_value = card.checkNumber(number)
            if card_value:
                cards_to_purge.append(card_index)

        cards_to_purge = list(set(cards_to_purge))
        cards_to_purge.sort()
        while len(cards_to_purge) != 0:
            print(number, cards_to_purge)
            bingo_cards.pop(cards_to_purge.pop())
    
    for number in bingo_calls:
        for card in bingo_cards:
            card_value = card.checkNumber(number)
            if card_value:
                printSolution(card_value)
                exit()



if __name__ == "__main__":
    main()