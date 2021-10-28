
def printSolution(x):
    print(f"The solution is {x}")

def main():
    frequency = 0
    f = open('input.txt', 'r')
    for l in f.readlines():
        frequency += int(l.strip())
        
    printSolution(frequency)

if __name__ == "__main__":
    main()