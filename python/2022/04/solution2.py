import re

def printSolution(x):
    print(f"The solution is: {x}")

def isOverlapping(a,b):
    for x in a:
        if b[0] <= x <= b[1]:
            return True
    for x in b:
        if a[0] <= x <= a[1]:
            return True
    return False

def main():
    file = open('../input/04.txt', 'r', encoding='utf-8')
    overlapCount = 0
    for line in file.readlines():
        min_a, max_a, min_b, max_b = [int(x) for x in re.split(r'[-,]',line.strip())]
        if isOverlapping((min_a, max_a), (min_b, max_b)):
            overlapCount += 1
    printSolution(overlapCount)


if __name__ == "__main__":
    main()