from collections import deque

def printSolution(x):
    print(f"The solution is {x}")

class SnailCalc:
    def __init__(self):
        self.number = ''

    def add(self, number):
        result = "[" + ','.join([self.number, number]) + "]"
        self.number = result
        self.reduce()
    
    def reduce(self):
        reducing = True
        while reducing:
            next_exp = self.findExplode()
            if next_exp != -1:
                self.explode(next_exp)
                continue
            next_split = self.findSplit()
            if next_split != -1:
                self.split(next_split)
                continue
            reducing = False

    def explode(self, idx):
        start, end = self.number[:idx-1], self.number[idx:]
        pair, end = end[:end.find(']')], end[end.find(']') + 1:]
        l, r = [int(x) for x in pair.split(',')]
        # insert left in start
        for idx in range(len(start) - 1, -1, -1):
            if start[idx].isdigit():
                start_1, start_2 = start[:idx+1], start[idx+1:]
                x = ''
                while start_1[-1].isdigit():
                    x += start_1[-1]
                    start_1 = start_1[:-1]
                x = x[::-1]
                x = int(x) + l
                start = start_1 + str(x) + start_2
                break
        # insert right in end
        for idx in range(len(end)):
            if end[idx].isdigit():
                end_1, end_2 = end[:idx], end[idx:]
                x = ''
                while end_2[0].isdigit():
                    x += end_2[0]
                    end_2 = end_2[1:]
                x = int(x) + r
                end = end_1 + str(x) + end_2
                break
        # insert zero in place
        self.number = start + '0' + end

    def split(self, idx):
        start, end = self.number[:idx], self.number[idx:]
        x = ''
        while end[0].isdigit():
            x += end[0]
            end = end[1:]
        half, extra = int(x)//2, int(x) % 2
        self.number = start + f"[{half},{half + extra}]" + end

    def magnitude(self):
        while not self.number.isdigit():
            for i, x in enumerate(self.number):
                if x.isdigit():
                    start, end = self.number[:i-1], self.number[i:]
                    pair, end = end[:end.find(']')], end[end.find(']') + 1:]
                    try:
                        l, r = [int(x) for x in pair.split(',')]
                        mag = 3 * l + 2 * r
                        self.number = start + str(mag) + end
                        break
                    except:
                        continue

    def findSplit(self):
        """ find and return index of next split
            if no splits exist, return -1 """
        for i, x in enumerate(self.number):
            if x.isdigit() and self.number[i + 1].isdigit():
                return i
        return -1

    def findExplode(self):
        """ find and return index of next exploding pair
            if no explosions exist, return -1 """
        depth = 0
        for i, x in enumerate(self.number):
            if x == '[':
                depth += 1
            elif x == ']':
                depth -= 1
            elif x.isdigit() and depth > 4:
                end = self.number[i:]
                pair = end[:end.find(']')]
                try:
                    l, r = [int(x) for x in pair.split(',')]
                    return i
                except:
                    continue
        return -1

def main():
    test = 'test.txt'
    puzzle = 'input.txt'
    active = puzzle

    numbers = []
    file = open(active, 'r')
    for line in file.readlines():
        numbers.append(line.strip())

    calc = SnailCalc()

    calc.number = numbers[0]

    for num in numbers[1:]:
        calc.add(num)

    calc.magnitude()
    printSolution(calc.number)


if __name__ == "__main__":
    main()
