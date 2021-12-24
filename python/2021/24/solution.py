
def printSolution(x):
    print(f"The solution is {x}")


class ALU:
    def __init__(self):
        self.w = 0
        self.x = 0
        self.y = 0
        self.z = 0
        self.input = 0
        self.program = []

    def store(self, a, b):
        if a == 'w':
            self.w = b
        elif a == 'x':
            self.x = b
        elif a == 'y':
            self.y = b
        elif a == 'z':
            self.z = b

    def inp(self, a):
        self.store(a, self.input)

    def add(self, a, b):
        x = self.getValue(a)
        b = self.getValue(b)
        self.store(a, x + b)

    def mul(self, a, b):
        x = getattr(self, a)
        b = self.getValue(b)
        self.store(a, x * b)

    def div(self, a, b):
        x = getattr(self, a)
        b = self.getValue(b)
        self.store(a, x//b)

    def mod(self, a, b):
        x = getattr(self, a)
        b = self.getValue(b)
        self.store(a, x % b)

    def eql(self, a, b):
        x = getattr(self, a)
        b = self.getValue(b)
        if x == b:
            self.store(a, 1)
        else:
            self.store(a, 0)

    def loadProgram(self, filename):
        file = open(filename, 'r')
        for line in file:
            self.program.append(line.strip())

    def loadInput(self, input):
        self.input = input

    def run(self):
        for inst in self.program:
            command = inst.split()
            func = getattr(self, command[0])
            func(*command[1:])

    def getValue(self, x):
        if x.isdigit():
            return int(x)
        else:
            return getattr(self, x)


def modelNumberGenerator():
    model_number = 99999999999999
    while True:
        yield model_number
        model_number -= 1


def main():
    a = ALU()
    a.loadProgram('test.txt')
    for x in range(17):
        a.loadInput(x)
        a.run()
        bin_val = int(''.join([str(a.w), str(a.x), str(a.y), str(a.z)]), 2)
        print(x, ":\t", a.w, a.x, a.y, a.z, "->", bin_val)

if __name__ == "__main__":
    main()
