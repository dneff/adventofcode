
def print_solution(x):
    print(f"The solution is: {x}")

class Computer():
    def __init__(self):
        self.progs = []
        self.instructions = []
        self.mapped = {}

    def run(self):
        if len(self.mapped) > 0:
            updated = [''] * 16
            for s,e in self.mapped.items():
                updated[e] = self.progs[s]
            self.progs = updated[:]

        for i in self.instructions:
            if i[0] == 's':
                x = int(i[1:])
                self.spin(x)
            elif i[0] == 'x':
                x,y = [int(x) for x in i[1:].split('/')]
                self.exchange(x,y)
            elif i[0] == 'p':
                x,y = [x for x in i[1:].split('/')]
                self.partner(x,y)

    def spin(self, a):
        self.progs = self.progs[-a:] + self.progs[:-a]

    def exchange(self, a, b):
        self.progs[a],self.progs[b] = self.progs[b],self.progs[a]

    def partner(self, a, b):
        idx_a = self.progs.index(a)
        idx_b = self.progs.index(b)
        self.progs[idx_a],self.progs[idx_b] = self.progs[idx_b], self.progs[idx_a]


def main():
    file = open('input.txt', 'r', encoding='utf-8')
    instructions = file.readline().strip().split(',')
    
    pc = Computer()
    pc.instructions = instructions
    start_prog = list('abcdefghijklmnop')

    pc.progs = start_prog[:]
    pc.run()

    repeating = []
    total_runs = 10000000000
    for cycle in range(1, total_runs + 1):
        pc.run()
        if pc.progs == start_prog:
            repeating.append(cycle)
        if len(repeating) >= 3:
            break

    cycle_size = repeating[-1] - repeating[-2]
    remaining_runs = total_runs - 1 - repeating[-1]
    remaining_runs = remaining_runs % cycle_size
    print(remaining_runs)
    for cycle in range(remaining_runs):
        pc.run()
        print_solution(''.join(pc.progs))

    print_solution(''.join(pc.progs))

if __name__ == "__main__":
    main()