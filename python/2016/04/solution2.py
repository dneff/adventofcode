import re
import string
from collections import defaultdict


def printSolution(x):
    print(f"The solution is: {x}")


def isRealRoom(name, checksum):
    count = defaultdict(int)
    for c in name:
        if c == "-":
            continue
        count[c] += 1

    frequency = defaultdict(list)
    for k, v in count.items():
        frequency[v].append(k)

    generated_sum = []
    for k in sorted(frequency.keys(), reverse=True):
        generated_sum.extend(sorted(frequency[k]))
    generated_sum = "".join([str(x) for x in generated_sum])
    if generated_sum[:5] == checksum:
        return True
    return False


def shiftCipher(s, rotations):
    result = []
    words = s.split("-")
    for word in words:
        for c in word:
            val = string.ascii_lowercase.find(c)
            new_val = (val + rotations) % len(string.ascii_lowercase)
            new_char = string.ascii_lowercase[new_val]
            result.append(new_char)
        result.append(" ")
    return "".join(result)


def main():
    file = open("input.txt", "r")

    words = defaultdict(int)
    sectors = {}
    for line in file:
        sector = re.search("(\d+)", line)[0]
        checksum = re.search("\[(.*)\]", line).group(1)
        name = line.split(sector)[0]
        if isRealRoom(name, checksum):
            sectors[sector] = shiftCipher(name, int(sector))
            for word in sectors[sector].split():
                words[word] += 1
    unique = []
    for k, v in words.items():
        if v == 1:
            unique.append(k)
    for k, v in sectors.items():
        if unique[0] in v:
            printSolution(k)


if __name__ == "__main__":
    main()
