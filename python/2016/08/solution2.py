
def printSolution(x):
    print(f"The solution is: {x}")


class cardReader():
    def __init__(self):
        self.height = 6
        self.width = 50
        self.screen = []
        for _ in range(self.height):
            row = ['.'] * self.width
            self.screen.append(row)

    def rect(self, w, h):
        for row in range(h):
            for col in range(w):
                self.screen[row][col] = '#'

    def rotateColumn(self, column, count):
        col = {}
        for row in range(self.height):
            col[row] = self.screen[row][column]
        for row in range(self.height):
            new_value = col[(row - count) % self.height]
            self.screen[row][column] = new_value

    def rotateRow(self, row, count):
        count = count % self.width
        self.screen[row] = self.screen[row][-count:] + \
            self.screen[row][:-count]

    def litCount(self):
        return sum([row.count('#') for row in self.screen])


def main():

    door = cardReader()

    file = open('input.txt', 'r')
    for line in file:
        line = line.strip()
        line = line.replace('x=', '')
        line = line.replace('y=', '')
        line = line.replace('by', '')
        line = line.replace('x', ' ')
        line = line.replace('rotate column', 'rotateColumn')
        line = line.replace('rotate row', 'rotateRow')
        line = line.split()

        instruction = getattr(door, line[0])
        instruction(int(line[1]), int(line[2]))

    for r in door.screen:
        row = ''.join(r)
        row = row.replace('.', ' ')
        print(row)


if __name__ == '__main__':
    main()
