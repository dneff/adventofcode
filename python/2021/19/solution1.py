import copy


def printSolution(x):
    print(f"The solution is {x}")


class Scanner:
    def __init__(self):
        self.id = 0
        self.beacons = []
        self.location = (0,0,0)
        self.rotation = 0

    def add(self, coordinates):
        self.beacons.append(coordinates)

    def rotate(self, rotations):
        pass


class Beacon:
    def __init__(self):
        self.location = (0,0,0)
        self.neighors = []
        self.scanner_count = 0


def main():
    test = 'test.txt'
    puzzle = 'input.txt'

    active = test

    scanners = []
    current_scanner = Scanner()

    file = open(active, 'r')
    for line in file.readlines():
        if len(line.strip()) == 0:
            scanners.append(current_scanner)
            current_scanner = Scanner()
            continue
        elif line[0] == '-':
            continue
        else:
            x, y, z = [int(x) for x in line.strip().split(',')]
            current_scanner.add((x, y, z))

    scanners.append(copy.copy(current_scanner))
    current_scanner.clear()

    for s in scanners:
        print(s)

if __name__ == "__main__":
    main()
