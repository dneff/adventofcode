def printSolution(x):
    print(f"The solution is: {x}")


class Calculator:
    def __init__(self):
        self.mem = []

    def parser(self, data):
        data_stack = []
        parsed = ""
        for idx in range(len(data)):
            if data[idx] == "(":
                data_stack.append(idx)
                parsed += " "
            elif data[idx] == ")":
                start = data_stack.pop()
                if not data_stack:
                    parsed += self.calculate(data[start + 1 : idx]) + " "
            elif not data_stack:
                parsed += data[idx]

        return self.calculate(parsed)

    def calculate(self, statement):
        if "(" in statement:
            statement = self.parser(statement)
        parse1 = [x for x in statement.split()]
        if len(parse1) == 1:
            return parse1[0]
        parse2 = []
        parse2.append(parse1.pop(0))
        while parse1:
            sign, y = parse1.pop(0), parse1.pop(0)
            if sign == "+":
                parse2[-1] = str(eval(parse2[-1] + sign + y))
            else:
                parse2.append(sign)
                parse2.append(y)

        return str(eval("".join(parse2)))


def main():
    file = open("input.txt", "r")

    calc = Calculator()

    for line in file:
        calc.mem.append(int(calc.parser(line)))

    printSolution(sum(calc.mem))


if __name__ == "__main__":
    main()
