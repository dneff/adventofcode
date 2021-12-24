
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
        x = self.getValue(a)
        b = self.getValue(b)
        self.store(a, x * b)

    def div(self, a, b):
        x = self.getValue(a)
        b = self.getValue(b)
        self.store(a, x//b)

    def mod(self, a, b):
        x = self.getValue(a)
        b = self.getValue(b)
        self.store(a, x % b)

    def eql(self, a, b):
        x = self.getValue(a)
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
        try:
            return int(x)
        except ValueError:
            return getattr(self, x)
        
    def clear(self):
        self.w = self.x = self.y = self.z = 0
        self.input = 0


def modelNumberGenerator():
    model_number = [9] * 14
    while True:
        yield int(''.join(map(str,model_number)))
        model_number[-1] -= 1
        for idx in range(len(model_number)-1,-1,-1):
            if model_number[idx] == 0:
                model_number[idx] = 9
                model_number[idx - 1] -= 1
            


def main():
    x = 13579246899999
    a = ALU()
    a.loadProgram('input.txt')

    model = modelNumberGenerator()
    while True:
        test_model = next(model)
        a.loadInput(test_model)
        a.run()
        if a.z == 0:
            printSolution(test_model)
            break
        a.clear()        

if __name__ == "__main__":
    main()
