
def print_solution(x):
    """prints input in solution format"""
    print(f"The solution is: {x}")


class GridMap():
    directions = {
        'n':  (0, -1, 1),
        'ne': (1, -1, 0),
        'se': (1, 0, -1),
        's': (0, 1, -1),
        'sw': (-1, 1, 0),
        'nw': (-1, 0, 1)
    }

    def __init__(self):
        self.loc = (0, 0, 0)

    def move(self, dir):
        diff = self.directions[dir]
        self.loc = (self.loc[0] + diff[0], self.loc[1] + diff[1], self.loc[2] + diff[2])

    def distance(self):
        distance = sum([abs(x) for x in list(self.loc)]) // 2
        return distance


def main():
    file = open('input.txt', 'r', encoding='utf-8')
    map = GridMap()
    moves = file.readline().strip().split(',')
    max_dist = 0
    for m in moves:
        map.move(m)
        max_dist = max(max_dist, map.distance())

    print_solution(max_dist)


if __name__ == "__main__":
    main()
