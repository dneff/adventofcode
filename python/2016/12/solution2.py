
def printSolution(x):
    print(f"The solution is {x}")

class BunnyPC():
    def __init__(self):
        self.register = {"a":0, "b":0, "c":0, "d":0}
        self.code = []
        self.instruction_pointer = 0

    def load(self, filename):
        file = open(filename, 'r')
        for line in file:
            self.code.append(line.strip())

    def resolveX(self, x):
        if x in "abcd":
            return self.register[x]
        return int(x)

    def cpy(self, x, y):
        #cpy x y copies x (either an integer or the value of a register) into register y.
        self.register[y] = self.resolveX(x)
        self.instruction_pointer += 1

    def inc(self, x):
        #inc x increases the value of register x by one.
        self.register[x] += 1
        self.instruction_pointer += 1

    def dec(self, x):
        #dec x decreases the value of register x by one.
        self.register[x] -= 1
        self.instruction_pointer += 1

    def jnz(self, x, y):
        #jnz x y jumps to an instruction y away (positive means forward; negative means backward), but only if x is not zero.
        if self.resolveX(x) != 0:
            self.instruction_pointer += int(y)
        else:
            self.instruction_pointer += 1

    def run(self):
        while self.instruction_pointer < len(self.code):
            inst = self.code[self.instruction_pointer].split()
            command = getattr(self, inst[0])
            command(*inst[1:])
        printSolution(self.register["a"])

def main():
    pc = BunnyPC()
    pc.register['c'] = 1
    pc.load('input.txt')
    pc.run()

if __name__ == "__main__":
    main()