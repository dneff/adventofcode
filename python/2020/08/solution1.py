from collections import defaultdict


def printSolution(x):
    print(f"The solution is: {x}")


"""a handheld game console"""


class Merlin:
    def __init__(self, data):
        self.accumulator = 0
        self.pointer = 0
        self.history = []
        self.instructions = data

        self.boot_load()

    def boot_load(self):

        loading = True
        while loading:
            self.history.append(self.pointer)
            inst = self.instructions[self.pointer]
            self.process_instruction(inst)
            loading = self.pointer not in self.history

    def process_instruction(self, inst):
        """ finds method and processes by returning it """
        i = getattr(self, inst[0])
        return i(inst[1])

    def nop(self, value):
        self.pointer += 1

    def acc(self, value):
        self.accumulator += value
        self.pointer += 1

    def jmp(self, value):
        self.pointer += value


def main():

    file = open("input.txt", "r")
    # format data to str, int pairs
    game_data = [line.strip() for line in file.readlines()]
    game_data = [i.split(" ") for i in game_data]
    for i in game_data:
        i[1] = int(i[1])

    game = Merlin(game_data)
    printSolution(game.accumulator)


if __name__ == "__main__":
    main()