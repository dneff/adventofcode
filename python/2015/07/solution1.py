def printSolution(x):
    print(f"The solution is: {x}")


class Circuit:
    def __init__(self):
        self.signals = {}

    def verify(self, *values):
        for x in values:
            if type(x) != int and not x.isnumeric() and x not in self.signals:
                return False
        return True

    def AND(self, left, right):
        if self.verify(left, right):
            values = []
            for x in [left, right]:
                if type(x) == int or x.isnumeric():
                    values.append(int(x))
                else:
                    values.append(self.signals[x])
            return values[0] & values[1]
        else:
            raise ValueError("no signal for wire")

    def OR(self, left, right):
        if self.verify(left, right):
            values = []
            for x in [left, right]:
                if x.isnumeric():
                    values.append(int(x))
                else:
                    values.append(self.signals[x])
            return values[0] | values[1]
        else:
            raise ValueError("no signal for wire")

    def LSHIFT(self, left, right):
        if self.verify(left, right):
            values = []
            for x in [left, right]:
                if x.isnumeric():
                    values.append(int(x))
                else:
                    values.append(self.signals[x])
            return values[0] << values[1]
        else:
            raise ValueError("no signal for wire")

    def RSHIFT(self, left, right):
        if self.verify(left, right):
            values = []
            for x in [left, right]:
                if x.isnumeric():
                    values.append(int(x))
                else:
                    values.append(self.signals[x])
            return values[0] >> values[1]
        else:
            raise ValueError("no signal for wire")

    def NOT(self, value):
        if self.verify(value):
            return ~int(value)
        else:
            raise ValueError("no signal for wire")

    def addWire(self, instruction):
        equation, value = instruction.split(" -> ")
        equation = equation.split()
        if len(equation) == 1:
            try:
                if self.verify(equation[0]):
                    if equation[0].isnumeric():
                        self.signals[value] = int(equation[0])
                    else:
                        self.signals[value] = self.signals[equation[0]]
                else:
                    return False
            except ValueError:
                return False
        elif len(equation) == 2:
            try:
                if self.verify(equation[1]):
                    self.signals[value] = self.NOT(self.signals[equation[1]])
                else:
                    return False
            except ValueError:
                return False
        else:
            left, operator, right = equation
            try:
                if self.verify(left, right):
                    self.signals[value] = getattr(self, operator)(left, right)
                else:
                    return False
            except ValueError:
                return False
        return True


def main():

    file = open("input.txt", "r")

    kit = Circuit()

    instructions = [line.strip() for line in file]

    while instructions:
        naughty = []

        for inst in instructions:
            if not kit.addWire(inst):
                naughty.append(inst)

        instructions = naughty[:]

    printSolution(kit.signals["a"])


if __name__ == "__main__":
    main()
