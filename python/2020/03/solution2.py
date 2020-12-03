class Map():
    ''' takes array of strings as input '''
    def __init__(self, data):
        self.data = data
        self.width = len(data[0])
        self.length = len(data)

    def getPointsOnSlope(self, x, y):
        ''' find all points on give slope '''
        points = []
        position = [0, 0]
        while position[1] < self.length:
            points.append(position[:])
            position[0] = (position[0] + x) % self.width
            position[1] += y
        return points

    def isTree(self, x, y):
        ''' check if position has a tree '''
        try:
            return self.data[y][x] == '#'
        except IndexError:
            print(f"bad point: {x, y} - width {self.width}, len {self.length}")


def printSolution(x):
    print(f"The solution is: {x}")


def main():
    file = open('input.txt', 'r')

    map_data = [line.strip() for line in file]
    map = Map(map_data)

    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]

    solution = 1
    for slope in slopes:
        s = [map.isTree(*x) for x in map.getPointsOnSlope(slope[0], slope[1])]
        print(f"Tree count for {slope} is {s.count(True)}")
        solution *= s.count(True)

    printSolution(solution)

if __name__ == "__main__":
    main()