"""solves 2023 Day 9 part 2"""


def print_solution(x):
    """prints solution"""
    print(f"The solution is: {x}")


def predict_previous(sequence):
    """return previous value in sequence"""
    diff = [y - x for x, y in zip(sequence, sequence[1:])]
    if len(set(diff)) == 1:
        return sequence[0] - diff[0]

    return sequence[0] - predict_previous(diff)


def main():
    """loads input and solves puzzle"""
    filename = "./python/2023/input/09.txt"
    lines = []
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]

    next_values = []
    for line in lines:
        sequence = [int(x) for x in line.split()]
        next_values.append(predict_previous(sequence))

    print_solution(sum(next_values))


if __name__ == "__main__":
    main()
