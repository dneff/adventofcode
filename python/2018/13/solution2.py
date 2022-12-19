
def printSolution(x):
    print(f"The solution is {x}")

class Train():

    def __init__(self, icon, location):
        self.icons = ['^', '>', 'v', '<']
        self.orientation = ['U','R','D','L']
        self.intersection = -1

        self.running = True
        self.direction = self.icons.index(icon)
        self.location = tuple(location)

        self.step = {
            'U': (0, -1),
            'R': (1, 0),
            'D': (0, 1),
            'L': (-1, 0)
        }

    def update_intersection(self):
        self.intersection += 1
        if self.intersection == 2:
            self.intersection = -1

    def move(self, world):
        if world[self.location] == '\\':
            if self.direction % 2 == 0:
                self.direction += -1
            else:
                self.direction += 1 

        if world[self.location] == '/':
            if self.direction % 2 == 0:
                self.direction += 1
            else:
                self.direction += -1

        if world[self.location] == '+':
            self.direction += self.intersection % 4
            self.update_intersection()

        self.direction = self.direction % 4

        heading = self.orientation[self.direction]
        self.location = tuple([x + y  for  x,y in zip(self.location, self.step[heading])])

    def __lt__(self, other):
        if self.location[1] < other.location[1]:
            return True
        elif self.location[1] == other.location[1]:
            return self.location[0] < other.location[0]
        return False

    def __repr__(self) -> str:
        return f"Train: {self.location}, {self.orientation[self.direction]}"


def main():
    test = 'test2.txt'
    puzzle = 'input.txt'

    active = puzzle

    file = open(active, 'r')

    world = {}
    trains = []
    for y, line in enumerate(file.readlines()):
        for x, char in enumerate(line.rstrip('\n')):
            if char != ' ':
                if char in ['^', 'v']:
                    trains.append(Train(char, (x,y)))
                    world[(x,y)] = '|'
                elif char in ['>', '<']:
                    trains.append(Train(char, (x,y)))
                    world[(x,y)] = '-'
                else:
                    world[(x,y)] = char

    ticks = 0
    while len(trains) > 1:
        trains.sort()
        for t in trains:
            if not t.running:
                continue
            t.move(world)

            train_locs = [tuple(x.location) for x in trains if x.running]            
            if len(set(train_locs)) != len(train_locs):
                for wrecked in trains:
                    if wrecked.location == t.location:
                        wrecked.running = False

        ticks += 1
        trains = [t for t in trains if t.running]

    printSolution(trains[0].location)


if __name__ == "__main__":
    main()