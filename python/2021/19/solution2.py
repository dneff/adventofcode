import copy
from collections import defaultdict


def printSolution(x):
    print(f"The solution is {x}")


def calculateRotations(beacons):
    variations = defaultdict(list)
    for beacon in beacons:
        x, y, z = beacon
        rotations = [
                (x, y, z), (x, -z, y), (x, -y, -z),
                (x, z, -y), (-x, -y, z), (-x, -z, -y),
                (-x, y, -z), (-x, z, y), (y, x, -z),
                (y, -x, z), (y, z, x), (y, -z, -x),
                (-y, x, z), (-y, -x, -z), (-y, -z, x),
                (-y, z, -x), (z, x, y), (z, -x, -y),
                (z, -y, x), (z, y, -x), (-z, x, -y),
                (-z, -x, y), (-z, y, x), (-z, -y, -x)
            ]

        for r_idx, r in enumerate(rotations):
            variations[r_idx].append(r)

    for k, v in variations.items():
        variations[k] = list(set(v))

    return variations


def manhattanDistance(a, b):
    xa, ya, za = a
    xb, yb, zb = b
    return abs(xb - xa) + abs(yb - ya) + abs(zb - za)


class Scanner:
    def __init__(self):
        self.id = 0
        self.beacons = []
        self.variations = {}
        self.location = (0, 0, 0)
        self.orientation = (1, 1, 1)
        self.rotation = 0

    def add(self, coordinates):
        self.beacons.append(coordinates)

    def addVariations(self):
        self.variations = calculateRotations(self.beacons)

    def calibrateLocation(self, location, variation):
        self.location = location
        self.beacons = [tuple(x - y for x, y in zip(location, z)) for z in variation]


def main():
    test = 'test.txt'
    puzzle = 'input.txt'

    active = puzzle

    scanners = []
    current_scanner = Scanner()

    file = open(active, 'r')
    for line in file.readlines():
        if len(line.strip()) == 0:
            current_scanner.addVariations()
            scanners.append(copy.copy(current_scanner))
            current_scanner = Scanner()
            continue
        elif line[:3] == '---':
            continue
        else:
            x, y, z = [int(x) for x in line.strip().split(',')]
            current_scanner.add((x, y, z))
    current_scanner.addVariations()
    scanners.append(copy.deepcopy(current_scanner))

    known_scanners = [scanners.pop(0)]
    known_beacons = []
    known_beacons.extend(known_scanners[0].beacons[:])

    # let's find shared beacons
    while len(scanners) > 0:
        matching = False
        test_scanner = scanners.pop(0)

        for v_idx, variation in test_scanner.variations.items():
            offsets = defaultdict(int)
            for beacon in known_beacons:
                for offset in variation:
                    xb, yb, zb = beacon
                    xo, yo, zo = offset
                    ship = (xo - xb, yo - yb, zo - zb)
                    offsets[ship] += 1
            for ship, count in offsets.items():
                if count >= 12:
                    matching = True
                    x, y, z = ship
                    test_scanner.location = (-x, -y, -z)
                    for beacon in variation:
                        xb, yb, zb = beacon
                        known_beacons.append((-x + xb, -y + yb, -z + zb))
                        known_scanners.append(copy.deepcopy(test_scanner))

        if not matching:
            scanners.append(test_scanner)

    locations = [scanner.location for scanner in known_scanners]
    distances = set()
    for idx, loc1 in enumerate(locations):
        for loc2 in locations[idx:]:
            distances.add(manhattanDistance(loc1, loc2))
    printSolution(max(distances))


if __name__ == "__main__":
    main()
