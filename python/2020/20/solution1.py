import math

def printSolution(x):
    print(f"The solution is: {x}")


class Tile:
    def __init__(self):
        self.id = None
        self.data = []
        self.edges = []
        self.connecting = []

    def getEdges(self):
        top, bottom = self.data[0], self.data[-1]
        left, right = [x[0] for x in self.data], [x[-1] for x in self.data]
        for v in [top, bottom, left, right]:
            self.edges.append(self.findValue(v))
            self.edges.append(self.findValue(v[::-1]))
        return self.edges

    def findValue(self, row):
        return int(''.join(row), 2)

    def __repr__(self):
        return repr(f"Tile: {self.id}, {self.data}")


def main():
    file = open("input.txt", "r")

    t = Tile()
    tiles = []
    for line in file:
        line = line.strip()
        if not line:
            t.getEdges()
            tiles.append(t)
            t = Tile()
        elif "Tile" in line:
            t.id = int("".join(filter(str.isdigit, line)))
        else:
            t.data.append(['1' if x == "#" else '0' for x in line])

    t.getEdges()
    tiles.append(t)

    for t in tiles:
        for t_check in tiles:
            if t.id == t_check.id:
                continue
            else:
                c = set(t.edges).intersection(set(t_check.edges))
                if len(c):
                    t.connecting.append(t_check.id)

    corners = [t for t in tiles if len(t.connecting) == 2]

    printSolution(math.prod([t.id for t in corners]))

if __name__ == "__main__":
    main()
