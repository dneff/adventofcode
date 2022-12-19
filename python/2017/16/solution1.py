
from socket import INADDR_MAX_LOCAL_GROUP


def print_solution(x):
    print(f"The solution is: {x}")

class Computer():
    def __init__(self):
        self.progs = list('abcdefghijklmnop')
        self.instructions = []


    def run(self):
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
    pc.run()
    print_solution(''.join(pc.progs))

    

if __name__ == "__main__":
    main()