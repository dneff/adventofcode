
def printSolution(x):
    print(f"The solution is: {x}")

def getUnique(a, b, c):
    return set(a).intersection(set(b), set(c)).pop()

def getValue(a):
    value = ord(a)
    value -= 96
    if value < 0:
        value += 32 + 26
    return value

def main():
    file = open('../input/03.txt', 'r', encoding='utf-8')
    result = 0
    chunk = []
    cycle = 0
    for line in file.readlines():
        chunk.append(line.strip())
        if cycle == 2:
            uni = getUnique(*chunk)
            result += getValue(uni)
            chunk.clear()
            cycle = -1
        cycle += 1

    printSolution(result)


if __name__ == "__main__":
    main()