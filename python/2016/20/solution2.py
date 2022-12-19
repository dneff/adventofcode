
def printSolution(x):
    print(f"The solution is {x}")

def main():

    blacklist = {}

    with open('input.txt', 'r') as f:
        for l in f.readlines():
            begin, end = l.strip().split('-')
            blacklist[int(begin)] = int(end)

    whitelist_floor = 0
    whitelisted = set()

    while len(blacklist.keys()) > 0:
        while len(blacklist.keys()) > 0 and min(blacklist.keys()) <= whitelist_floor:
            whitelist_floor = max(whitelist_floor, blacklist[min(blacklist.keys())] + 1)
            blacklist.pop(min(blacklist.keys()))

        if len(blacklist.keys()) > 0:
            whitelisted.add(whitelist_floor)
            whitelist_floor += 1

    printSolution(len(whitelisted))

if __name__ == "__main__":
    main()