def printSolution(x):
    print(f"The solution is: {x}")


def propertyOne(s):
    """checks if any pair appears twice"""
    for idx in range(1, len(s)):
        pair = s[idx - 1: idx + 1]
        if pair in s[: idx - 1] or pair in s[idx + 1:]:
            return True
    return False


def propertyTwo(s):
    """checks if any character repeats with a letter in between"""
    for idx in range(2, len(s)):
        if s[idx] == s[idx - 2]:
            return True
    return False


def main():

    file = open("input.txt", "r")

    nice = []
    naughty = []

    for line in file:
        line = line.strip()
        if all([propertyOne(line), propertyTwo(line)]):
            nice.append(line)
        else:
            naughty.append(line)

    printSolution(len(nice))


if __name__ == "__main__":
    main()
