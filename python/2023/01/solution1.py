def print_solution(x):
    """Prints the solution"""
    print(f"The solution is: {x}")


def first_last_int(string):
    """Returns the first and last integer in a string"""
    ints = [c for c in string if c.isdigit()]
    return int("".join([ints[0], ints[-1]]))


def main():
    """finds solution"""
    file = open("../input/01.txt", "r", encoding="UTF-8")
    lines = file.readlines()
    file.close()
    values = [first_last_int(line.strip()) for line in lines]
    print_solution(sum(values))


if __name__ == "__main__":
    main()
