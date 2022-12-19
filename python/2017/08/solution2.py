from collections import defaultdict
from dis import Instruction

def print_solution(x):
    print(f"The solution is: {x}")


class Computer():
    def __init__(self):
        self.instructions = []
        self.register = defaultdict(int)
        self.max_mem = 0

    def run(self):
        for i in self.instructions:
            inst = 'self.register[\'' + i[0] + '\']'
            if i[1] == 'inc':
                inst = f"{inst} += {i[2]}" 
            else:
                inst = f"{inst} -= {i[2]}" 
            cond = f"self.register['{i[4]}'] {i[5]} {i[6]}"

            if eval(cond):
                exec(inst)
                self.max_mem = max(self.max_mem, max(self.register.values()))


def main():
    pc = Computer()
    file = open('input.txt', 'r', encoding='utf-8')
    for line in file.readlines():
        pc.instructions.append(line.strip().split())

    pc.run()

    print_solution(pc.max_mem)


if __name__ == "__main__":
    main()