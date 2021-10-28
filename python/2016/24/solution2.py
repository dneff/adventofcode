from queue import PriorityQueue
from itertools import permutations

def printSolution(x):
    print(f"The solution is {x}")

class Map():
    def __init__(self):
        self.valid = set()
        self.POI = {}

    def prune(self):
        max_row = max([x[0] for x in self.valid])
        max_col = max([x[1] for x in self.valid])
        dead_ends = 1
        while dead_ends > 0:
            dead_ends = 0
            for r in range(max_row+1):
                for c in range(max_col+1):
                    if (r,c) in self.valid and (r, c) not in self.POI.values():
                        if len(self.findAdjacent((r, c))) <= 1:
                            self.valid.remove((r, c))
                            dead_ends += 1

    def display(self):
        max_row = max([x[0] for x in self.valid])
        max_col = max([x[1] for x in self.valid])
        for r in range(max_row+1):
            row = ''
            for c in range(max_col+1):
                if (r, c) in self.POI.values():
                    row += str(list(self.POI.keys())[list(self.POI.values()).index((r, c))])
                elif (r, c) in self.valid:
                    row += '.'
                else:
                    row += ' '
            print(row)

    def addValid(self, x):
        if x not in self.valid:
            self.valid.add(x)
    
    def addPOI(self, x, y):
        self.POI[x] = y
        self.addValid(y)

    def findAdjacent(self, loc):
        result = []
        x,y = loc
        possible = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        for p in possible:
            if p in self.valid:
                result.append(p)
        return result

    def findDistance(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def findPath(self, src, dest):
        seen_locations = set()
        next_location = PriorityQueue()

        next_location.put((0, (src, 0)))

        while not next_location.empty():
            _, data = next_location.get()
            seen_locations.add(data[0])
            steps = data[-1] + 1
            if steps >= 748:
                continue
            adjacent = self.findAdjacent(data[0])
            for loc in adjacent:
                if loc not in seen_locations:
                    if loc == dest:
                        return steps
                    score = self.findDistance(src, loc) + steps * steps
                    next_location.put((score, (loc, steps)))

def main():

    ducts = Map()

    file = open('input.txt', 'r')
    for row, l in enumerate(file.readlines()):
        for col, c in enumerate(l):
            if c == '.':
                ducts.addValid((row, col))
            if c.isdigit():
                ducts.addPOI(int(c), (row, col))
    
    distances = {}

    ducts.prune()
    #ducts.display()

    #shortest_path = min(paths.keys())
    #current_location = paths[min(paths.keys())][-1][-1]
    shortest_path = 502
    current_location = 5
 
    return_dist = ducts.findPath(ducts.POI[0], ducts.POI[current_location])

    #747 wrong
    # 748 high
    # 752 high
    print(return_dist + shortest_path)
        





if __name__ == "__main__":
    main()