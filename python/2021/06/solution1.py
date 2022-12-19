import copy

def printSolution(x):
    print(f"The solution is {x}")


class LanternFishSchool():
    def __init__(self):
        self.school = {
            0: 0,
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 0,
            7: 0,
            8: 0
        }
        self.day = 0

    def loadState(self, data):
        for x in data:
            self.school[x] += 1

    def advance(self):
        result = dict.fromkeys(self.school, 0)
        for k, v in self.school.items():
            if k == 0:
                result[6] += v
                result[8] += v
            else:
                result[k-1] += v
        self.school = copy.deepcopy(result)
        self.day += 1

    def countFish(self):
        return sum([v for k, v in self.school.items()])

    def sumFish(self):
        return sum([k*v for k, v in self.school.items()])


def main():
    number_of_days = 80

    puzzle = 'input.txt'
    test = 'test.txt'
    active = puzzle

    file = open(active, 'r')
    data = [int(x) for x in file.readline().strip().split(',')]

    school = LanternFishSchool()

    school.loadState(data)

    for day in range(number_of_days):
        school.advance()

    printSolution(school.countFish())


if __name__ == "__main__":
    main()
