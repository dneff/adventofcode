
def advanceReader(x):
    return x + 4

def add(inst, prog):
    prog[inst[2]] = prog[inst[0]] + prog[inst[1]]    

def multiply(inst, prog):
    prog[inst[2]] = prog[inst[0]] * prog[inst[1]]    

def processProgram(prog):
    reader = 0
    while True:
        instruction = prog[reader]
        if instruction == 99:
            break
        elif instruction == 1:
            add(prog[reader+1:reader+4], prog)
        elif instruction == 2:
            multiply(prog[reader+1:reader+4], prog)
        
        reader = advanceReader(reader)

    return prog[0]


def main():
    with open('input1.txt', 'r') as file:
        content = file.read()
        initial_prog = [int(x)for x in content.strip().split(',')]

    target_output = 19690720

    for a in range(100):
        for b in range(100):
            test_prog = initial_prog[:]
            test_prog[1] = a
            test_prog[2] = b
            
            test_output = processProgram(test_prog)

            if test_output == target_output:
                print(f"The solution is: {a * 100 + b}")
                break



if __name__ == "__main__":
    main()