import re

def printSolution(x):
    print(f"The solution is: {x}")

def isSubset(a,b):
    cmp1 = a[0] <= b[0]
    cmp2 = a[1] >= b[1]
    if cmp1 and cmp2:
        return True
    cmp1 = b[0] <= a[0]
    cmp2 = b[1] >= a[1]
    if cmp1 and cmp2:
        return True
    return False

def main():
    file = open('../input/04.txt', 'r', encoding='utf-8')
    subsetCount = 0
    for line in file.readlines():
        min_a, max_a, min_b, max_b = [int(x) for x in re.split(r'[-,]',line.strip())]
        if isSubset((min_a, max_a), (min_b, max_b)):
            subsetCount += 1
    printSolution(subsetCount)


if __name__ == "__main__":
    main()