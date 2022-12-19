from collections import deque

class InputInterrupt(Exception):
    pass

class OutputInterrupt(Exception):
    pass

class IntCode:

    def __init__(self, prog, *args):
        self.debugging = False
        self.complete = False
        self.memory = [int(x)for x in prog.strip().split(',')] + [0] * 200000
        self.reader = 0
        self.relative_base = 0
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
            8: self.i_equals,
            9: self.i_base_adjust
        }

        i_param_count = {
            1: 3,
            2: 3,
            3: 1,
            4: 1,
            5: 2,
            6: 2,
            7: 3,
            8: 3,
            9: 1
        }
        return i_func[i], i_param_count[i]

    def i_add(self, params):
        self.memory[params[2]] = params[0] + params[1]
        self.advanceReader(len(params) + 1)

    def i_multiply(self, params):
        self.memory[params[2]] = params[0] * params[1]
        self.advanceReader(len(params) + 1)

    def i_input(self, params):
        try:
            self.memory[params[0]] = self.input.popleft()
        except(IndexError):
            raise InputInterrupt
        else:
            self.advanceReader(len(params) + 1)

    def i_output(self, params):
        self.output.append(params[0])
        self.advanceReader(len(params) + 1)
        raise OutputInterrupt

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

    def i_base_adjust(self, params):
        self.relative_base += params[0]
        self.advanceReader(len(params) + 1)
    
    def setModes(self, x):
        result = [int(x) for x in str(x).zfill(3)[::-1]]
        return result[:len(str(x))]

    def resolveParameters(self, params, modes, opcode):
        resolved = params[:]
        for idx, val in enumerate(self.setModes(modes)[:len(params)]):
            if val == 0:
                resolved[idx] = self.memory[params[idx]]
            elif val == 1:
                resolved[idx] = params[idx]
            elif val == 2:
                if opcode not in [3] and idx < 2:
                    resolved[idx] = self.memory[params[idx] + self.relative_base]
                else:
                    resolved[idx] = params[idx] + self.relative_base

        return resolved

    def run(self):
        while not self.complete:
            modes, opcode = divmod(self.memory[self.reader], 100)
            #self.debug(f"DEBUG: reader {self.reader}, relative base: {self.relative_base}, opcode {opcode}, modes {modes} {self.setModes(modes)}")
            if opcode == 99:
                self.complete = True
                break

            operation, param_cnt = self.getOperation(opcode)
            p_start = self.reader + 1
            p_end = p_start + param_cnt
            #self.debug(f"DEBUG: reader {self.reader}, mem val: {self.memory[self.reader]}, relative base: {self.relative_base}, opcode {opcode}, modes {modes} {self.setModes(modes)}, mid params {self.memory[p_start:p_end]}")
            params = self.resolveParameters(self.memory[p_start:p_end], modes, opcode)
            #if modes >= 200:
            self.debug(f"DEBUG: reader {self.reader},  mem val: {self.memory[self.reader]}, relative base: {self.relative_base}, opcode {opcode}, modes {modes} {self.setModes(modes)}, final params {params}")
            #self.debug("---")
            operation(params)

    def debug(self, x):
        if self.debugging:
            print(x)
