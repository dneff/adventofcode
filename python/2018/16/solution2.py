import copy
import ast
from collections import defaultdict

def printSolution(x):
    print(f"The solution is {x}")


class WristCalc:
    def __init__(self):
        self.registers = [0] * 4
        self.commands = {}
        self.command_names = [
            'addr', 'addi', 'mulr', 'muli',
            'banr', 'bani', 'borr', 'bori',
            'setr', 'seti',
            'gtri', 'gtir', 'gtrr',
            'eqri', 'eqir', 'eqrr'
        ]
        for idx, c in enumerate(self.command_names):
            func = getattr(self, c)
            self.commands[idx] = func

    def setRegisters(self, values):
        for i, x in enumerate(values):
            self.registers[i] = x

    def getRegisters(self):
        return self.registers

    def reset(self):
        self.registers = [0] * 4

    def run(self, f, a, b, c):
        self.commands[f](a, b, c)

    def addr(self, a, b, c):
        # (add register) stores into register C
        # the result of adding register A and register B.
        self.registers[c] = self.registers[a] + self.registers[b]

    def addi(self, a, b, c):
        # (add immediate) stores into register C
        # the result of adding register A and value B.
        self.registers[c] = self.registers[a] + b

    def mulr(self, a, b, c):
        # (multiply register) stores into register C
        # the result of multiplying register A
        # and register B.
        self.registers[c] = self.registers[a] * self.registers[b]

    def muli(self, a, b, c):
        # (multiply immediate) stores into
        # register C the result of multiplying
        # register A and value B.
        self.registers[c] = self.registers[a] * b

    def banr(self, a, b, c):
        # (bitwise AND register) stores into
        # register C the result of the bitwise
        # AND of register A and register B.
        self.registers[c] = self.registers[a] & self.registers[b]

    def bani(self, a, b, c):
        # (bitwise AND immediate) stores into
        # register C the result of the bitwise AND
        # of register A and value B.
        self.registers[c] = self.registers[a] & b

    def borr(self, a, b, c):
        # (bitwise OR register) stores into
        # register C the result of the bitwise OR
        # of register A and register B.
        self.registers[c] = self.registers[a] | self.registers[b]

    def bori(self, a, b, c):
        # (bitwise OR immediate) stores into
        # register C the result of the bitwise OR
        # of register A and value B.
        self.registers[c] = self.registers[a] | b

    def setr(self, a, b, c):
        # (set register) copies the contents of
        # register A into register C.
        # (Input B is ignored.)
        self.registers[c] = self.registers[a]

    def seti(self, a, b, c):
        # (set immediate) stores value A
        # into register C. (Input B is ignored.)
        self.registers[c] = a

    def gtir(self, a, b, c):
        # (greater-than immediate/register) sets
        # register C to 1 if value A is greater
        # than register B. Otherwise, register C is set to 0.
        if a > self.registers[b]:
            self.registers[c] = 1
        else:
            self.registers[c] = 0

    def gtri(self, a, b, c):
        # (greater-than register/immediate) sets
        # register C to 1 if register A is greater
        # than value B. Otherwise, register C is set to 0.
        if self.registers[a] > b:
            self.registers[c] = 1
        else:
            self.registers[c] = 0

    def gtrr(self, a, b, c):
        # (greater-than register/register) sets
        # register C to 1 if register A is greater
        # than register B. Otherwise, register C is set to 0.
        if self.registers[a] > self.registers[b]:
            self.registers[c] = 1
        else:
            self.registers[c] = 0

    def eqir(self, a, b, c):
        # (equal immediate/register) sets register C
        # to 1 if value A is equal to register B.
        # Otherwise, register C is set to 0.
        if a == self.registers[b]:
            self.registers[c] = 1
        else:
            self.registers[c] = 0

    def eqri(self, a, b, c):
        # (equal register/immediate) sets register C
        # to 1 if register A is equal to value B.
        # Otherwise, register C is set to 0.
        if self.registers[a] == b:
            self.registers[c] = 1
        else:
            self.registers[c] = 0

    def eqrr(self, a, b, c):
        # (equal register/register) sets register C
        # to 1 if register A is equal to register B.
        # Otherwise, register C is set to 0.
        if self.registers[a] == self.registers[b]:
            self.registers[c] = 1
        else:
            self.registers[c] = 0


def main():
    file = open('input.txt', 'r')
    calc = WristCalc()
    tests = []
    test = {}
    empty = 0
    for line in file.readlines():
        data = line.strip()
        if not data:
            empty += 1
            if len(test.keys()) > 0:
                tests.append(copy.deepcopy(test))
                test.clear()
            if empty == 3:
                break
            continue

        if data[0] == 'B':
            b = data.split(': ')[-1]
            test['before'] = ast.literal_eval(b)
            empty = 0
        elif data[0] == 'A':
            a = data.split(':  ')[-1]
            test['after'] = ast.literal_eval(a)
            empty = 0
        else:
            test['input'] = [int(x) for x in data.split()]
            empty = 0

    file.close()
    file = open('input.txt', 'r')
    instructions = []
    empty = 0
    seeking = True
    for line in file.readlines():
        if seeking:
            data = line.strip()
            if not data:
                empty += 1
                if empty == 3:
                    seeking = False
            else:
                empty = 0
            continue
        instructions.append([int(x) for x in line.strip('\n').split()])

    # iterate through the tests. If there's a test with
    # only one possible command, add it to new_command
    # and stop testing for it. This should iteratively
    # filter the tested commands down to zero.

    new_command = defaultdict(str)
    hunting = True
    while hunting:
        match2 = defaultdict(list)
        mappings = defaultdict(set)

        for idx_t, test in enumerate(tests):
            for f in range(16):
                if test['input'][0] in new_command.keys():
                    continue
                calc.setRegisters(test['before'])
                calc.commands[f](*test['input'][1:])
                if calc.getRegisters() == test['after'] and calc.command_names[f] not in new_command.values():
                    match2[idx_t].append(calc.command_names[f])
                calc.reset()

        for k, v in match2.items():
            if len(v) == 1:
                mappings[v[0]].add(tests[k]['input'][0])

        for k, v in mappings.items():
            if len(v) == 1:
                new_command[v.pop()] = k

        if len(new_command.keys()) == len(calc.command_names):
            hunting = False

    # load new commands into calc
    for idx, c in new_command.items():
        func = getattr(calc, c)
        calc.commands[idx] = func

    # run instructions and get result
    calc.reset()
    for i in instructions:
        calc.run(*i)

    printSolution(calc.registers[0])


if __name__ == "__main__":
    main()
