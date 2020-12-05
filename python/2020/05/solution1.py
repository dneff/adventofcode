def printSolution(x):
    print(f"The solution is: {x}")


def ticketToRowSeatId(ticket):
    row = ticket[:7].replace("F", "0").replace("B", "1")
    row = int(row, 2)

    seat = ticket[7:].replace("L", "0").replace("R", "1")
    seat = int(seat, 2)

    id = row * 8 + seat

    return row, seat, id


def main():

    file = open("input.txt", "r")

    ids = []
    for line in file:
        row, seat, id = ticketToRowSeatId(line.strip())
        ids.append(id)

    printSolution(max(ids))


if __name__ == "__main__":
    main()