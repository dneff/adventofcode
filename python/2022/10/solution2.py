

class Device:
    def __init__(self):
        self.instructions = []
        self.cycle = 0
        self.index = 0
        self.X = 1
        row = [' '] * 40
        self.CRT = [row.copy() for i in range(6)]

    def noop(self):
        self.addCycle()
        self.index += 1

    def addx(self, value):
        self.addCycle()
        self.addCycle()
        self.X += value
        self.index += 1
    
    def isDrawn(self):
        position = self.cycle % 40
        return self.X in [position, position + 1, position - 1]

    def draw(self):
        row = self.cycle // 40
        col = self.cycle % 40
        self.CRT[row][col] = '#'

    def addCycle(self):
        if self.isDrawn():
            self.draw()
        self.cycle = self.cycle + 1
        if self.cycle == 241:
            self.cycle == 1

    def run(self):
        while self.index < len(self.instructions):
            instruction = self.instructions[self.index]
            if instruction == 'noop':
                self.noop()
            elif instruction.startswith('addx'):
                value = int(instruction.split(' ')[1])
                self.addx(value)

def main():
    file = open('../input/10.txt', 'r', encoding='utf-8')
    instructions = file.read().splitlines()
    d = Device()
    d.instructions = instructions
    d.run()

    for row in d.CRT:
        print(''.join(row))
    print()

if __name__ == "__main__":
    main()