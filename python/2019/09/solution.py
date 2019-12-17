from itertools import permutations
from IntCode import IntCode, InputInterrupt, OutputInterrupt


def main():
    with open('input1.txt', 'r') as file:
        program = file.read().strip()

    comp = IntCode(program)
    #comp = IntCode("109, 1, 3, 3, 204, 2, 99") # equals input
    comp.push(1)

    while not comp.complete:
        try:
            comp.run()
        except(OutputInterrupt):
            pass

    print(f"Solution 1: The final output is {comp.pop()}")

    comp2 = IntCode(program)
    #comp2.debugging = True
    comp2.push(2)

    while not comp2.complete:
        try:
            comp2.run()
        except(OutputInterrupt):
            pass
    #print(f"reader is {comp2.reader}")
    print(f"Solution 2: The final output is {comp2.output[-1]}")
    
    

if __name__ == "__main__":
    main()
