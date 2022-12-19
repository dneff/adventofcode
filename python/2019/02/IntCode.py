class IntCode:

    def __init__(self, prog, *args):
        self.complete = False
        self.memory = [int(x)for x in prog.strip().split(',')]
        self.reader = 0
        self.input = []
        self.output = []

        if args:
            self.input = args[:]

    def advanceReader(self, x):
        self.reader += x

    def prog_add(self, inst):
        self.memory[inst[2]] = self.memory[inst[0]] + self.memory[inst[1]]
        self.advanceReader(4)

    def prog_multiply(self, inst):
        self.memory[inst[2]] = self.memory[inst[0]] * self.memory[inst[1]]
        self.advanceReader(4)
    
    def run(self):
        while not self.complete:
            opcode = self.memory[self.reader] % 100
            if opcode == 99:
                self.complete = True
                break
            elif opcode == 1:
                self.prog_add(self.memory[self.reader + 1:self.reader + 4])
            elif opcode == 2:
                self.prog_multiply(self.memory[self.reader + 1:self.reader + 4])
