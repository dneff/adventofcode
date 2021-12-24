

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

    def loadProgram(self, data):
        self.program.clear()
        self.program = data[:]

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
        self.program.clear()


def main():

    programs = []
    file = open('input.txt')
    # break into 14 distinct programs
    prog = []
    for idx, line in enumerate(file.readlines()):
        if idx % 18 == 0 and idx != 0:
            programs.append(prog[:])
            prog.clear()
        prog.append(line.strip())
    programs.append(prog[:])

    prog.clear()

    modifiers = {}
    for p_idx in range(len(programs)):
        div = int(programs[p_idx][4].split()[-1])
        check = int(programs[p_idx][5].split()[-1])
        offset = int(programs[p_idx][-3].split()[-1])
        modifiers[p_idx] = (div, check, offset)

    offsets = []
    primary = {}
    for k in range(len(modifiers.keys())):
        div, check, offset = modifiers[k][0], modifiers[k][1], modifiers[k][2]
        if check > 0:
            offsets.append((k, offset))
        else:
            inp, offs = offsets.pop()
            print(f"input[{k}] == input[{inp}] + {check+offs}")
            primary[inp] = (k, check+offs)

    # can now compute minimum
    model = [0] * 14
    for k, v in primary.items():
        second, offset = v
        if offset > 0:
            model[k], model[second] = 1, 1 + offset
        else:
            model[second], model[k] = 1, 1 - offset

    max_model = int(''.join([str(x) for x in model]))

    printSolution(max_model)


if __name__ == "__main__":
    main()
