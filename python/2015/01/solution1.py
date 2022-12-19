
def printSolution(x):
    print(f"The solution is: {x}")


def main():

    file = open("input.txt", "r")

    floor = 0
    buttons = {
        '(': 1,
        ')': -1
    }

    for push in file.readline():
        floor += buttons[push]

    printSolution(floor)


if __name__ == "__main__":
    main()
