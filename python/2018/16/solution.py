
from typing_extensions import ParamSpecArgs


def printSolution(x):
    print(f"The solution is {x}")


class WristCalc:
    def __init__(self):
        self.registers = [0] * 4

    def setRegisters(self, values):
        for i, x in enumerate(values):
            self.registers[i] = x

    def getRegisters(self):
        return self.registers

    def addr(self,a, b, c):
        # (add register) stores into register C
        # the result of adding register A and register B.
        pass

    def addi(self,a, b, c):
        # (add immediate) stores into register C 
        # the result of adding register A and value B.
        pass

    def mulr(self,a, b, c):
        # (multiply register) stores into register C 
        # the result of multiplying register A 
        # and register B.
        pass

    def muli(self,a, b, c):
        # (multiply immediate) stores into 
        # register C the result of multiplying 
        # register A and value B.
        pass

    def banr(self,a, b, c):
        # (bitwise AND register) stores into 
        # register C the result of the bitwise 
        # AND of register A and register B.
        pass

    def bani(self,a, b, c):
        # (bitwise AND immediate) stores into 
        # register C the result of the bitwise AND
        # of register A and value B.
        pass

    def borr(self,a, b, c):
        # (bitwise OR register) stores into 
        # register C the result of the bitwise OR
        # of register A and register B.
        pass

    def bori(self,a, b, c):
        # (bitwise OR immediate) stores into 
        # register C the result of the bitwise OR
        # of register A and value B.
        pass

    def setr(self,a, b, c):
        # (set register) copies the contents of 
        # register A into register C. 
        # (Input B is ignored.)
        pass

    def seti(self,a, b, c):
        # (set immediate) stores value A 
        # into register C. (Input B is ignored.)
        pass

    def gtir(self,a, b, c):
        # (greater-than immediate/register) sets 
        # register C to 1 if value A is greater 
        # than register B. Otherwise, register C is set to 0.
        pass

    def gtri(self,a, b, c):
        # (greater-than register/immediate) sets 
        # register C to 1 if register A is greater 
        # than value B. Otherwise, register C is set to 0.
        pass

    def gtrr(self,a, b, c):
        # (greater-than register/register) sets 
        # register C to 1 if register A is greater 
        # than register B. Otherwise, register C is set to 0.
        pass

    def eqir(self,a, b, c):
        # (equal immediate/register) sets register C 
        # to 1 if value A is equal to register B. 
        # Otherwise, register C is set to 0.
        pass

    def eqri(self,a, b, c):
        # (equal register/immediate) sets register C 
        # to 1 if register A is equal to value B. 
        # Otherwise, register C is set to 0.
        pass

    def eqrr(self,a, b, c):
        # (equal register/register) sets register C 
        # to 1 if register A is equal to register B. 
        # Otherwise, register C is set to 0.
        pass


def main():
    file = open('test.txt', 'r')
    for line in file.readlines():
        print(line.strip())


if __name__ == "__main__":
    main()
