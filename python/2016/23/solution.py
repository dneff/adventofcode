import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2016/23/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils

class BunnyPC():
    def __init__(self):
        self.register = {"a":0, "b":0, "c":0, "d":0}
        self.code = []
        self.instruction_pointer = 0

    def load(self, filename):
        lines = AoCInput.read_lines(filename)
        for line in lines:
            self.code.append(line.strip())

    def resolveX(self, x):
        if x in "abcd":
            return self.register[x]
        return int(x)

    def cpy(self, x, y):
        # cpy x y copies x (either an integer or the value of a register) into register y.
        self.register[y] = self.resolveX(x)
        self.instruction_pointer += 1

    def inc(self, x):
        # inc x increases the value of register x by one.
        self.register[x] += 1
        self.instruction_pointer += 1

    def dec(self, x):
        # dec x decreases the value of register x by one.
        self.register[x] -= 1
        self.instruction_pointer += 1

    def mul(self, x, y, z):
        # mul x y z stores the multiple of y and z in register x.
        self.register[x] += self.resolveX(y) * self.resolveX(z)
        self.instruction_pointer += 1

    def jnz(self, x, y):
        #jnz x y jumps to an instruction y away 
        # (positive means forward; negative means backward)
        # but only if x is not zero.
        if self.resolveX(x) != 0:
            self.instruction_pointer += self.resolveX(y)
        else:
            self.instruction_pointer += 1
    
    def tgl(self, x):
        # For one-argument instructions, inc becomes dec, and all other one-argument instructions become inc.
        # For two-argument instructions, jnz becomes cpy, and all other two-instructions become jnz.
        # The arguments of a toggled instruction are not affected.
        # If an attempt is made to toggle an instruction outside the program, nothing happens.
        # If toggling produces an invalid instruction (like cpy 1 2) and an attempt is later made to execute that instruction, skip it instead.
        # If tgl toggles itself (for example, if a is 0, tgl a would target itself and become inc a), the resulting instruction is not executed until the next time it is reached.
        toggle_pointer = self.instruction_pointer + self.register[x]
        if toggle_pointer < 0 or toggle_pointer > (len(self.code) - 1):
            self.instruction_pointer += 1
            return
        toggle_inst = self.code[toggle_pointer].split()
        if len(toggle_inst) == 2:
            if toggle_inst[0] == 'inc':
                toggle_inst[0] = 'dec'
            else:
                toggle_inst[0] = 'inc'
        elif len(toggle_inst) == 3:
            if toggle_inst[0] == 'jnz':
                toggle_inst[0] = 'cpy'
            else:
                toggle_inst[0] = 'jnz'
        self.code[toggle_pointer] = ' '.join(toggle_inst)
        #print(self.code[toggle_pointer], toggle_inst)
        self.instruction_pointer += 1           


    def run(self):
        while self.instruction_pointer < len(self.code):
            inst = self.code[self.instruction_pointer].split()
            command = getattr(self, inst[0])
            command(*inst[1:])
            #print(inst, self.register, self.code)
        AoCUtils.print_solution(1, self.register["a"])

def main():
    test = 0
    puzzle1 = 7
    puzzle2 = 12

    active = puzzle2

    pc = BunnyPC()
    pc.register['a'] = active
    pc.load(INPUT_FILE)
    pc.run()
    # 239500799

if __name__ == "__main__":
    main()
