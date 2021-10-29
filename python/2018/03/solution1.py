from collections import defaultdict

def printSolution(x):
    print(f"The solution is {x}")

def main():
    fabric = defaultdict(int)

    file = open('input.txt', 'r')
    for line in file.readlines():
        _, _,loc, size = line.strip().split()
        x, y = [int(x) for x in loc[:-1].split(',')]
        width, height = [int(x) for x in size.split('x')]

        for w in range(width):
            for h in range(height):
                fabric_spot = (x+w, y+h)
                fabric[fabric_spot] += 1

    overlaps = [k for k,v in fabric.items() if v > 1]
    printSolution(len(overlaps))

if __name__ == "__main__":
    main()