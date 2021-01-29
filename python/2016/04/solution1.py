import re
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


def main():
    file = open("input.txt", "r")

    sector_ids = []
    for line in file:
        sector = re.search("(\d+)", line)[0]
        checksum = re.search("\[(.*)\]", line).group(1)
        name = line.split(sector)[0]
        if isRealRoom(name, checksum):
            sector_ids.append(int(sector))
    printSolution(sum(sector_ids))


if __name__ == "__main__":
    main()
