def printSolution(x):
    print(f"The solution is: {x}")

def main():
    file = open('input.txt', 'r')
    x = 0
    treeCount = 0

    for line in file:
        l = line.strip()
        if l[x%len(l)] == '#':
            treeCount += 1
        x += 3

    printSolution(treeCount) 

if __name__ == "__main__":
    main()