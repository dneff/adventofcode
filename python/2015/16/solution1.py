from collections import defaultdict


def printSolution(x):
    print(f"The solution is: {x}")


def main():

    file = open("input.txt", "r")

    detected = {
        "children": 3,
        "cats": 7,
        "samoyeds": 2,
        "pomeranians": 3,
        "akitas": 0,
        "vizslas": 0,
        "goldfish": 5,
        "trees": 3,
        "cars": 2,
        "perfumes": 1,
    }
    

    aunts = {}
    matches = defaultdict(int)
    for line in file:
        line = line.strip().lstrip("Sue ")
        line = line.replace(":", "").replace(",", "")
        line = line.split()

        aunt = int(line.pop(0))
        aunts[aunt] = {}
        while line:
            k, v = line.pop(0), line.pop(0)
            aunts[aunt][k] = int(v)

    for aunt, details in aunts.items():
        for k, v in details.items():
            if k in detected and detected[k] == v:
                matches[aunt] += 1

    printSolution(max(matches, key=matches.get))


if __name__ == "__main__":
    main()
