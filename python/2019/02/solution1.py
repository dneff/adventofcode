
def advanceReader(x):
    return x + 4

def add(inst, prog):
    print(f"adding {inst}")
    prog[inst[2]] = prog[inst[0]] + prog[inst[1]]    

def multiply(inst, prog):
    print(f"multiplying {inst}")
    prog[inst[2]] = prog[inst[0]] * prog[inst[1]]    

def main():
    with open('input1.txt', 'r') as file:
        content = file.read()
        prog = [int(x)for x in content.strip().split(',')]

    reader = 0

    while True:
        instruction = prog[reader]
        print(f"current instruction: {prog[reader:reader+4]}")
        if instruction == 99:
            break
        elif instruction == 1:
            add(prog[reader+1:reader+4], prog)
        elif instruction == 2:
            multiply(prog[reader+1:reader+4], prog)
        
        reader = advanceReader(reader)

    print(f"The solution is: {prog[0]}")



if __name__ == "__main__":
    main()