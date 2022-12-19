
def printSolution(x):
    print(f"The solution is {x}")


def main():
    file = open('input.txt', 'r')

    depths = [int(x) for x in file.readlines()]
    windows = [x+y+z for x,y,z in zip(depths, depths[1:], depths[2:])]
    diffs = [y-x for x,y in zip(windows, windows[1:])]
    deeper_soundings = sum([1 for x in diffs if x > 0])
    printSolution(deeper_soundings)

if __name__ == "__main__":
    main()