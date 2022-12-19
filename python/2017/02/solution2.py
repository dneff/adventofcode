
def printSolution(x):
    print(f"The solution is: {x}")


def main():
    f = open('input.txt', 'r')
    row_div = []
    for row in f.readlines():
        r = [int(x) for x in row.split()]
        r.sort(reverse=True)

        for i, x in enumerate(r):
            for y in r[i+1:]:
                if x % y == 0:
                    row_div.append(x//y)
    printSolution(sum(row_div))


if __name__ == "__main__":
    main()
