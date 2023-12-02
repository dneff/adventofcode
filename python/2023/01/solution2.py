numbers = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def print_solution(x):
    """Prints the solution"""
    print(f"The solution is: {x}")


def first_last_int(string):
    """Returns the first and last integer in a string"""
    first, last = None, None
    for i, c in enumerate(string):
        if c.isdigit():
            if first is None:
                first = int(c)
            last = int(c)
        else:
            if i < len(string) - 2 and string[i : i + 3] in numbers:
                if first is None:
                    first = numbers[string[i : i + 3]]
                last = numbers[string[i : i + 3]]
            elif i < len(string) - 3 and string[i : i + 4] in numbers:
                if first is None:
                    first = numbers[string[i : i + 4]]
                last = numbers[string[i : i + 4]]
            elif i < len(string) - 4 and string[i : i + 5] in numbers:
                if first is None:
                    first = numbers[string[i : i + 5]]
                last = numbers[string[i : i + 5]]
    return first * 10 + last


def main():
    """find solution"""
    file = open("./python/2023/input/01.txt", "r", encoding="utf-8")
    lines = file.readlines()
    file.close()

    values = [first_last_int(line.strip()) for line in lines]
    print_solution(sum(values))


if __name__ == "__main__":
    main()
