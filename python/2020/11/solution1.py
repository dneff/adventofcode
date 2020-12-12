def printSolution(x):
    print(f"The solution is: {x}")


class WaitingRoom:
    def __init__(self, data):
        self.time = 0
        self.seats = self.getSeats(data)

        self.adjacent = {}
        for s in self.seats.keys():
            self.adjacent[s] = self.getAdjacent(s)

    def getSeats(self, data):
        seats = {}
        for r, line in enumerate(data):
            for c, seat in enumerate(line):
                if seat == "L":
                    seats[(r, c)] = False
        return seats

    def getAdjacent(self, seat):
        offsets = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)]
        possibleLocations = [tuple(map(sum, zip(seat, o))) for o in offsets]
        return [x for x in possibleLocations if x in self.seats]

    def getNeighbors(self, seat):
        return sum([self.seats[s] for s in self.adjacent[seat]])

    def updateSeats(self):
        newSeats = {}
        for s, o in self.seats.items():
            if o:
                newSeats[s] = self.getNeighbors(s) <= 3
            else:
                newSeats[s] = self.getNeighbors(s) == 0
        self.seats = newSeats
        self.time += 1

    def getPeople(self):
        return sum(self.seats.values())


def main():
    file = open("input.txt", "r")

    data = [line.strip() for line in file.readlines()]
    room = WaitingRoom(data)
    count = room.getPeople()
    changing = True
    while changing:
        room.updateSeats()
        changing = room.getPeople() != count
        count = room.getPeople()

    printSolution(room.getPeople())


if __name__ == "__main__":
    main()