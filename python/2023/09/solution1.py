"""solves 2023 Day 9 part 1"""


def print_solution(x):
    """prints solution"""
    print(f"The solution is: {x}")


def predict_next(sequence):
    """return next value in sequence"""
    diff = [y - x for x, y in zip(sequence, sequence[1:])]
    if len(set(diff)) == 1:
        return sequence[-1] + diff[0]

    return sequence[-1] + predict_next(diff)


def main():
    """loads input and solves puzzle"""
    filename = "./python/2023/input/09.txt"
    lines = []
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]

    next_values = []
    for line in lines:
        sequence = [int(x) for x in line.split()]
        next_values.append(predict_next(sequence))

    print_solution(sum(next_values))

if __name__ == "__main__":
    main()
