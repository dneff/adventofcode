from collections import defaultdict

def print_solution(x):
    """format input for printing"""
    print(f"The solution is: {x}")

class Turing():
    def __init__(self):
        self.cycles = 0
        self.state = getattr(self, 'state_a')
        self.tape = defaultdict(int)
        self.cursor = 0

    def run(self, cycles):
        self.cycles = cycles
        while self.cycles > 0:
            self.state()
            self.cycles -= 1
            if self.cycles % 100000 == 0:
                print(f"{self.cycles}/{cycles}")

    def checksum(self):
        return sum(self.tape.values())

    def state_a(self):
        if self.tape[self.cursor] == 0:
            self.tape[self.cursor] = 1
            self.cursor += 1
            self.state = getattr(self, 'state_b')
        else:
            self.tape[self.cursor] = 0
            self.cursor += 1
            self.state = getattr(self, 'state_f')

    def state_b(self):
        if self.tape[self.cursor] == 0:
            self.tape[self.cursor] = 0
            self.cursor -= 1
            self.state = getattr(self, 'state_b')
        else:
            self.tape[self.cursor] = 1
            self.cursor -= 1
            self.state = getattr(self, 'state_c')

    def state_c(self):
        if self.tape[self.cursor] == 0:
            self.tape[self.cursor] = 1
            self.cursor -= 1
            self.state = getattr(self, 'state_d')
        else:
            self.tape[self.cursor] = 0
            self.cursor += 1
            self.state = getattr(self, 'state_c')

    def state_d(self):
        if self.tape[self.cursor] == 0:
            self.tape[self.cursor] = 1
            self.cursor -= 1
            self.state = getattr(self, 'state_e')
        else:
            self.tape[self.cursor] = 1
            self.cursor += 1
            self.state = getattr(self, 'state_a')

    def state_e(self):
        if self.tape[self.cursor] == 0:
            self.tape[self.cursor] = 1
            self.cursor -= 1
            self.state = getattr(self, 'state_f')
        else:
            self.tape[self.cursor] = 0
            self.cursor -= 1
            self.state = getattr(self, 'state_d')

    def state_f(self):
        if self.tape[self.cursor] == 0:
            self.tape[self.cursor] = 1
            self.cursor += 1
            self.state = getattr(self, 'state_a')
        else:
            self.tape[self.cursor] = 0
            self.cursor -= 1
            self.state = getattr(self, 'state_e')

    def __str__(self):
        tape_idx = list(self.tape.keys())
        tape_idx.sort()
        return f"{[self.tape[x] for x in tape_idx]}"

def main():
    pc = Turing()
    pc.run(12425180)

    print_solution(pc.checksum())


if __name__ == "__main__":
    main()