from itertools import permutations

def advanceReader(x, size):
    return x + size

def setModes(x):
    modes = {
        0: [0, 0],
        1: [1, 0],
        10: [0, 1],
        11: [1, 1]
    }
    return modes[x]

def resolveParameters(args, params, prog):
    resolved = args[:]
    for idx, val in enumerate(params):
        if val == 0:
            resolved[idx] = prog[args[idx]]
        elif val == 1:
            resolved[idx] = args[idx]
    return resolved

def add(args, prog):
    prog[args[2]] = args[0] + args[1]    

def multiply(args, prog):
    prog[args[2]] = args[0] * args[1]    

def input(inst, prog_input, prog):
    prog[inst] = prog_input

def output(inst, prog):
    return prog[inst]
    print(f"output: {prog[inst]}")

def processProgram(prog, *args):
    reader = 0
    prog_input = list(args[::-1])
    prog_output = []

    while True:
        modes, instruction = divmod(prog[reader], 100)
        params = setModes(modes)

        if instruction == 99:
            #end
            break
        elif instruction == 1:
            #add
            args = resolveParameters(prog[reader + 1: reader + 4], params, prog)
            add(args, prog)
            reader = advanceReader(reader, len(args) + 1)
        elif instruction == 2:
            #multiply
            args = resolveParameters(prog[reader + 1: reader + 4], params, prog)
            multiply(args, prog)
            reader = advanceReader(reader, len(args) + 1)
        elif instruction == 3:
            #input
            input(prog[reader + 1], prog_input.pop(), prog) 
            reader = advanceReader(reader, 2)
        elif instruction == 4:
            #output
            prog_output.append(output(prog[reader + 1], prog))
            reader = advanceReader(reader, 2)
        elif instruction == 5:
            #jump-if-true
            args = resolveParameters(prog[reader + 1: reader + 3], params, prog)
            if args[0] != 0:
                reader = args[1]
            else:
                reader = advanceReader(reader, 3)
        elif instruction == 6:
            #jump-if-false
            args = resolveParameters(prog[reader + 1: reader + 3], params, prog)
            if args[0] == 0:
                reader = args[1]
            else:
                reader = advanceReader(reader, 3)
        elif instruction == 7:
            #less than
            args = resolveParameters(prog[reader + 1: reader + 4], params, prog)
            if args[0] < args[1]:
                prog[args[2]] = 1
            else:
                prog[args[2]] = 0
            reader = advanceReader(reader, 4)
        elif instruction == 8:
            #equals
            args = resolveParameters(prog[reader + 1: reader + 4], params, prog)
            if args[0] == args[1]:
                prog[args[2]] = 1
            else:
                prog[args[2]] = 0
            reader = advanceReader(reader, 4)
        
    return prog_output.pop()


def main():
    with open('input1.txt', 'r') as file:
        content = file.read()
        initial_prog = [int(x)for x in content.strip().split(',')]

    max_thrust = 0
    phases = [x for x in range(5)]
    for phase_order in list(permutations(phases, len(phases))):
        thrust = 0
        for phase in phase_order:
            thrust = processProgram(initial_prog, phase, thrust)
        max_thrust = max(max_thrust, thrust)
    
    print(f"The max thrust is: {max_thrust}")

        


if __name__ == "__main__":
    main()