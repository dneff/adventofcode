from collections import deque


class IntCode:

    def __init__(self, prog, *args):
        self.complete = False
        self.memory = [int(x)for x in prog.strip().split(',')]
        self.reader = 0
        self.input = deque()
        self.output = deque()

        if args:
            self.input = args[:]

    def pop(self):
        return self.output.popleft()

    def push(self, x):
        self.input.append(x)

    def advanceReader(self, x):
        self.reader += x

    def getOperation(self, i):
        i_func = {
            1: self.i_add,
            2: self.i_multiply,
            3: self.i_input,
            4: self.i_output,
            5: self.i_jump_true,
            6: self.i_jump_false,
            7: self.i_less_than,
            8: self.i_equals
        }

        i_param_count = {
            1: 3,
            2: 3,
            3: 1,
            4: 1,
            5: 2,
            6: 2,
            7: 3,
            8: 3
        }
        return i_func[i], i_param_count[i]

    def i_add(self, params):
        self.memory[params[2]] = params[0] + params[1]
        self.advanceReader(len(params) + 1)

    def i_multiply(self, params):
        self.memory[params[2]] = params[0] * params[1]
        self.advanceReader(len(params) + 1)

    def i_input(self, params):
        x = self.input.popleft()
        self.memory[params[0]] = x
        self.advanceReader(len(params) + 1)

    def i_output(self, params):
        self.output.append(self.memory[params[0]])
        self.advanceReader(len(params) + 1)

    def i_jump_true(self, params):
        if params[0] != 0:
            self.reader = params[1]
        else:
            self.advanceReader(len(params) + 1)

    def i_jump_false(self, params):
        if params[0] == 0:
            self.reader = params[1]
        else:
            self.advanceReader(len(params) + 1)

    def i_less_than(self, params):
        if params[0] < params[1]:
            self.memory[params[2]] = 1
        else:
            self.memory[params[2]] = 0
        self.advanceReader(len(params) + 1)

    def i_equals(self, params):
        if params[0] == params[1]:
            self.memory[params[2]] = 1
        else:
            self.memory[params[2]] = 0
        self.advanceReader(len(params) + 1)

    def setModes(self, x):
        modes = {
            0: [0, 0],
            1: [1, 0],
            10: [0, 1],
            11: [1, 1]
        }
        return modes[x]

    def resolveParameters(self, params, modes):
        resolved = params[:]
        for idx, val in enumerate(self.setModes(modes)[:len(params)]):
            if val == 0:
                resolved[idx] = self.memory[params[idx]]
            elif val == 1:
                resolved[idx] = params[idx]

        return resolved

    def run(self):
        while not self.complete:
            modes, opcode = divmod(self.memory[self.reader], 100)
            if opcode == 99:
                self.complete = True
                break

            operation, param_cnt = self.getOperation(opcode)
            p_start = self.reader + 1
            p_end = p_start + param_cnt
            if opcode in [1, 2, 5, 6, 7, 8]:
                params = self.resolveParameters(self.memory[p_start:p_end], modes)
            else:
                params = self.memory[p_start:p_end]
            operation(params)
