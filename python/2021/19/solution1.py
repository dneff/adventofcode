import copy


def printSolution(x):
    print(f"The solution is {x}")

class Scanner:
    def __init__(self):
        self.id = 0
        self.beacons = []
        self.orientation = (0,0,0)

    def add(self, coordinates):
        self.beacons.append(coordinates)

    def rotate(self, rotations):
        pass

def main():
    test = 'test.txt'
    puzzle = 'input.txt'

    active = test

    scanners = []
    current_scanner = []

    file = open(active, 'r')
    for line in file.readlines():
        if len(line.strip()) == 0:
            scanners.append(copy.copy(current_scanner))
            current_scanner.clear()
            continue
        elif line[0] == '-':
            continue
        else:
            x, y, z = [int(x) for x in line.strip().split(',')]
            current_scanner.append([x, y, z])

    scanners.append(copy.copy(current_scanner))
    current_scanner.clear()

    for s in scanners:
        print(s)

if __name__ == "__main__":
    main()
