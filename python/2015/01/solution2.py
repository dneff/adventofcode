
def printSolution(x):
    print(f"The solution is: {x}")


def main():

    file = open("input.txt", "r")

    floor = 0
    buttons = {
        '(': 1,
        ')': -1
    }

    for count, push in enumerate(file.readline()):
        floor += buttons[push]
        if floor == -1:
            printSolution(count + 1)
            break


if __name__ == "__main__":
    main()
