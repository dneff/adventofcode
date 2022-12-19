from collections import defaultdict


def printSolution(x):
    print(f"The solution is: {x}")


def propertyOne(s):
    """checks string contains at least 3 vowels"""
    chars = defaultdict(int)
    for c in s:
        chars[c] += 1

    vowel_count = sum([chars[x] for x in ["a", "e", "i", "o", "u"]])

    return vowel_count >= 3


def propertyTwo(s):
    """checks at least one letter appears twice in a row"""
    for idx, c in enumerate(s):
        if idx == 0:
            continue
        if c == s[idx - 1]:
            return True
    return False


def propertyThree(s):
    """checks no forbidden pairs are in string"""
    bad_pairs = ["ab", "cd", "pq", "xy"]
    for pair in bad_pairs:
        if pair in s:
            return False
    return True


def main():

    file = open("input.txt", "r")

    nice = []
    naughty = []

    for line in file:
        line = line.strip()
        if all([propertyOne(line), propertyTwo(line), propertyThree(line)]):
            nice.append(line)
        else:
            naughty.append(line)

    printSolution(len(nice))


if __name__ == "__main__":
    main()
