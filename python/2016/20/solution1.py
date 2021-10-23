
def printSolution(x):
    print(f"The solution is {x}")

def main():

    blacklist = {}

    with open('input.txt', 'r') as f:
        for l in f.readlines():
            begin, end = l.strip().split('-')
            blacklist[int(begin)] = int(end)

    whitelist_floor = 0

    while min(blacklist.keys()) <= whitelist_floor:
        whitelist_floor = max(whitelist_floor, blacklist[min(blacklist.keys())] + 1)
        blacklist.pop(min(blacklist.keys()))

    printSolution(whitelist_floor)

if __name__ == "__main__":
    main()