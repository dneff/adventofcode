def printSolution(x):
    print(f"The solution is: {x}")


class Computer:
    def __init__(self):
        self.index = 0
        self.registers = {"a": 0, "b": 0}
        self.instructions = []

    def load(self, data):
        for line in data:
            self.instructions.append(line.strip().split())

    def run(self):
        while self.index < len(self.instructions):
            inst = self.instructions[self.index]
            command = getattr(self, inst[0])
            if len(inst) == 2:
                command(inst[-1])
            else:
                command(inst[1][0], inst[-1])

    def hlf(self, r):
        self.registers[r] = self.registers[r] // 2
        self.index += 1

    def tpl(self, r):
        self.registers[r] *= 3
        self.index += 1

    def inc(self, r):
        self.registers[r] += 1
        self.index += 1

    def jmp(self, offset):
        self.index += int(offset)

    def jie(self, r, offset):
        if self.registers[r] % 2 == 0:
            self.index += int(offset)
        else:
            self.index += 1

    def jio(self, r, offset):
        if self.registers[r] == 1:
            self.index += int(offset)
        else:
            self.index += 1


def main():

    gift = Computer()

    file = open("input.txt", "r")
    gift.load(file.readlines())

    gift.run()

    printSolution(gift.registers['b'])


if __name__ == "__main__":
    main()
