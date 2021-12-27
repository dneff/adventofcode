from collections import defaultdict
import copy
import math


def printSolution(x):
    print(f"The solution is {x}")


class Scanner:
    def __init__(self):
        self.id = 0
        self.beacons = []
        self.vectors = {}
        self.location = (0, 0, 0)
        self.rotation = 0

    def add(self, coordinates):
        self.beacons.append(coordinates)

    def rotate(self, rotations):
        pass

    def calculateVectors(self):
        for s_idx in range(len(self.beacons)):
            for d_idx in range(s_idx + 1, len(self.beacons)):
                distance = (d - s for s, d in zip(self.beacons[s_idx], self.beacons[d_idx]))
                x, y, z = distance
                vector = math.sqrt(x**2 + y**2 + z**2)
                self.vectors[round(vector, 1)] = [s_idx, d_idx]


class Beacon:
    def __init__(self):
        self.location = (0, 0, 0)
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
            current_scanner.calculateVectors()
            scanners.append(current_scanner)
            current_scanner = Scanner()
            continue
        elif line[:3] == '---':
            continue
        else:
            x, y, z = [int(x) for x in line.strip().split(',')]
            current_scanner.add((x, y, z))

    current_scanner.calculateVectors()
    scanners.append(copy.copy(current_scanner))
    current_scanner = Scanner()

    shared = set(scanners[0].vectors.keys()).intersection(set(scanners[4].vectors.keys()))
    shared_b = set()
    for v in shared:
        for b in scanners[0].vectors[v]:
            shared_b.add(scanners[0].beacons[b])
    for b in shared_b:
        print(b)
    print(len(shared_b))

if __name__ == "__main__":
    main()
