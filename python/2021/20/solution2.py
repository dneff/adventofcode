from collections import defaultdict
import copy


def printSolution(x):
    print(f"The solution is {x}")


class ImageProcessor:
    def __init__(self):
        self.enhancements = 0
        self.algorithm = ''
        self.image = defaultdict(lambda: '0')

    def getAlgoValue(self, position):
        px, py = position
        algo_idx = ''
        for y in [py-1, py, py+1]:
            for x in [px-1, px, px+1]:
                algo_idx += self.image[(x, y)]
        return self.algorithm[int(algo_idx, 2)]

    def enhance(self):
        if self.enhancements % 2 == 1:
            new_image = defaultdict(lambda: '1')
            self.image.default_factory = lambda: '1'
        else:
            new_image = defaultdict(lambda: '0')
            self.image.default_factory = lambda: '0'

        min_r = min([x[1] for x in self.image.keys()])
        max_r = max([x[1] for x in self.image.keys()])
        min_c = min([x[0] for x in self.image.keys()])
        max_c = max([x[0] for x in self.image.keys()])
        for r in range(min_r-1, max_r + 2):
            for c in range(min_c-1, max_c + 2):
                e = self.getAlgoValue((c, r))
                if e == '#':
                    new_image[(c, r)] = '1'
                else:
                    new_image[(c, r)] = '0'

        self.image = copy.deepcopy(new_image)
        self.enhancements += 1

    def getPixelCount(self):
        pixels = [1 for x in self.image.values() if x == '1']
        return sum(pixels)

    def __repr__(self) -> str:
        result = '\n'
        min_r = min([x[1] for x in self.image.keys()])
        max_r = max([x[1] for x in self.image.keys()])
        min_c = min([x[0] for x in self.image.keys()])
        max_c = max([x[0] for x in self.image.keys()])
        for r in range(min_r, max_r + 1):
            for c in range(min_c, max_c + 1):
                if self.image[(c, r)] == '1':
                    result += '#'
                else:
                    result += ' '
            result += '\n'
        return result


def main():
    test = 'test.txt'
    puzzle = 'input.txt'

    ip = ImageProcessor()

    file = open(puzzle, 'r')

    ip.algorithm = file.readline().strip()

    file.readline()

    for y, line in enumerate(file.readlines()):
        for x, pixel in enumerate(line):
            if pixel == '#':
                ip.image[(x, y)] = '1'
            else:
                ip.image[(x, y)] = '0'

    steps = 50
    for _ in range(steps):
        ip.enhance()

    printSolution(ip.getPixelCount())


if __name__ == "__main__":
    main()
