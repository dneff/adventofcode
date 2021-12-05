def printSolution(x):
    print(f"The solution is {x}")

class Sub:
    def __init__(self):
        self.position = 0
        self.depth = 0
    
    def forward(self, x):
        self.position += x

    def up(self, x):
        self.depth -= x

    def down(self, x):
        self.depth += x

    def solution(self):
        return self.position * self.depth

def main():

    sub = Sub()

    file = open('input.txt', 'r')
    for line in file.readlines():
        direction, distance = line.strip().split()
        command = getattr(sub, direction)
        command(int(distance))

    printSolution(sub.solution())
        


if __name__ == "__main__":
    main()