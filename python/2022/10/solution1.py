
def printSolution(x):
    print(f"The solution is: {x}")

class Device:
    def __init__(self):
        self.instructions = []
        self.cycle = 0
        self.index = 0
        self.X = 1
        self.criticalCycles = {k: 0 for k in [20, 60, 100, 140, 180, 220]}

    def noop(self):
        self.addCycle()
        self.index += 1

    def addx(self, value):
        self.addCycle()
        self.addCycle()
        self.X += value
        self.index += 1

    def signalStrength(self):
        return self.cycle * self.X
    
    def addCycle(self):
        self.cycle += 1
        if self.cycle in self.criticalCycles:
            print(f"Cycle {self.cycle}: X = {self.X}: strength = {self.signalStrength()}")
            self.criticalCycles[self.cycle] = self.signalStrength()

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
    printSolution(sum(d.criticalCycles.values()))

if __name__ == "__main__":
    main()