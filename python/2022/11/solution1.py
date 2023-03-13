
def printSolution(x):
    print(f"The solution is: {x}")

class Monkey:
    def __init__(self):
        self.items = []
        self.operator = ""
        self.testVal = 1
        self.testTrue = 1
        self.testFalse = 0
        self.inspectCount = 0

    def worry(self, old):
        return eval(self.operator) // 3

    def inspect(self, item):
        if item % self.testVal == 0:
            return self.testTrue
        return self.testFalse

    def turn(self, monkeys):
        while self.items:
            self.inspectCount += 1
            item = self.items.pop()
            item = self.worry(item)
            monkeys[self.inspect(item)].items.append(item)

def main():
    file = open('../input/11.txt', 'r', encoding='utf-8')

    monkeys = []
    for line in file:
        if line.startswith('Monkey'):
            monkeys.append(Monkey())
        elif 'Starting' in line:
            monkeys[-1].items = [int(x) for x in line.strip().split(': ')[-1].split(',')]
        elif 'Operation' in line:
            monkeys[-1].operator = line.strip().split('= ')[-1]
        elif 'Test' in line:
            monkeys[-1].testVal = int(line.strip().split('by ')[-1])
        elif 'true' in line:
            monkeys[-1].testTrue = int(line.strip().split('monkey ')[-1])
        elif 'false' in line:
            monkeys[-1].testFalse = int(line.strip().split('monkey ')[-1])

    rounds = 20
    for i in range(rounds):
        for monkey in monkeys:
            monkey.turn(monkeys)

    monkeyBusiness = [monkey.inspectCount for monkey in monkeys]
    monkeyBusiness.sort()
    #print(monkeyBusiness)
    #for idx, monkey in enumerate(monkeys):
    #    print(f"Monkey {idx}: {monkey.items}")
    
    printSolution(monkeyBusiness[-1] * monkeyBusiness[-2])

if __name__ == '__main__':
    main()
