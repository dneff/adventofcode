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

    file = open('input.txt', 'r')
    for line in file.readlines():
        id, _,loc, size = line.strip().split()
        x, y = [int(x) for x in loc[:-1].split(',')]
        width, height = [int(x) for x in size.split('x')]
        
        claim_locs = []
        for w in range(width):
            for h in range(height):
                fabric_spot = (x+w, y+h)
                claim_locs.append(fabric[fabric_spot] == 1)

        if all(claim_locs):
            printSolution(id[1:])
            break
        




if __name__ == "__main__":
    main()