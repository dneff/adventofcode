
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

    
def main():
    file = open('test.txt', 'r')
    for line in file.readlines():
        print(line.strip())


if __name__ == "__main__":
    main()
