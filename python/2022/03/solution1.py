
def printSolution(x):
    print(f"The solution is: {x}")

def getUnique(a, b):
    return set(a).intersection(set(b)).pop()

def getValue(a):
    value = ord(a)
    value -= 96
    if value < 0:
        value += 32 + 26
    return value

def main():
    file = open('../input/03.txt', 'r', encoding='utf-8')
    result = 0
    for line in file.readlines():
        middle = len(line) // 2
        a, b = line.strip()[:middle], line.strip()[middle:]
        uni = getUnique(a,b)
        result += getValue(uni)

    printSolution(result)


if __name__ == "__main__":
    main()