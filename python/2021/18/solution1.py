
def printSolution(x):
    print(f"The solution is {x}")

class SnailCalc:
    def __init__(self):
        self.number = []
    
    def add(self, number):
        pass
    
    def simplify(self):
        pass
    
    def explode(self):
        pass
    
    def split(self):
        pass
    
    def magnitud(self):
        pass
    
def main():
    test = 'test.txt'
    puzzle = 'input.txt'
    active = test
    file = open(active, 'r')
    for line in file.readlines():
        print(line.strip())


if __name__ == "__main__":
    main()