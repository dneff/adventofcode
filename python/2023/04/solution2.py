def print_solution(x):
    """prints solution"""
    print(f"The solution is: {x}")


def main():
    """solves day 4 part 2"""
    filename = "./python/2023/input/04.txt"
    cards = {}
    with open(filename, "r", encoding="utf-8") as file:
        for idx, line in enumerate(file.readlines()):
            winners, numbers = line.strip().split(":")[1].split(" | ")
            winners = [int(x) for x in winners.split()]
            numbers = [int(x) for x in numbers.split()]
            cards[idx + 1] = {"winners": winners[:], "numbers": numbers[:], "count": 1}

    for card_id, card in cards.items():
        matches = len(set(card["winners"]) & set(card["numbers"]))
        if matches:
            for new_card in range(1, matches + 1):
                cards[card_id + new_card]["count"] += card["count"]

    card_counts = [card["count"] for card in cards.values()]

    print_solution(sum(card_counts))


if __name__ == "__main__":
    main()
