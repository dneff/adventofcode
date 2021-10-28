
def printSolution(x):
    print(f"The solution is {x}")

def main():
    frequency = 0
    seen = set()
    seeking = True

    while seeking:
        f = open('input.txt', 'r')
        for l in f.readlines():
            frequency += int(l.strip())
            if frequency in seen:
                seeking = False
                break
            else:
                seen.add(frequency)
        f.close()
    printSolution(frequency)

if __name__ == "__main__":
    main()