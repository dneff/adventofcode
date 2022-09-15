from collections import defaultdict
from string import ascii_lowercase as letters

def print_solution(x):
    """format input for printing"""
    print(f"The solution is {x}")

class Duet():
    """simulated computer"""
    def __init__(self, id):
        self.id = id
        self.duet = None
        self.program = []
        self.buffer = []
        self.tx_count = 0
        self.mul_count = 0
        self.pointer = 0
        self.locked = False
        self.registers = defaultdict(int)

    def run(self):
        """executes the instructions and advances instruction pointer
        until out of range of instruction list"""
        while -1 < self.pointer < len(self.program):
            instruction = self.program[self.pointer]
            i = getattr(self, instruction[0])
            i(*instruction[1:],)
            if instruction[0] != 'jnz':
                self.pointer += 1
            if self.locked == True:
                return
        self.locked = True
        return


    def set(self, x, y):
        """sets register X to the value of Y"""
        self.registers[x] = self.get(y)

    def sub(self, x, y):
        """decreases register X by the value of Y"""
        self.registers[x] -= self.get(y)

    def mul(self, x, y):
        """sets register X to the result of multiplying
        the value contained in register X by the value of Y"""
        self.registers[x] *= self.get(y)
        self.mul_count += 1

    def jnz(self, x, y):
        """jumps with an offset of the value of Y,
        but only if the value of X is not zero.
        (An offset of 2 skips the next instruction, an
        offset of -1 jumps to the previous instruction, and so on.)"""

        if self.get(x) != 0:
            self.pointer += self.get(y)
        else:
            self.pointer += 1

    def get(self,x):
        if x in letters:
            return self.registers[x]
        else:
            return int(x)


def main():
    pc0 = Duet(0)

    file = open('input.txt', 'r', encoding='utf-8')
    for line in file.readlines():
        pc0.program.append(line.strip().split())

    while not pc0.locked:
        pc0.run()

    print_solution(pc0.mul_count)


if __name__ == "__main__":
    main()
