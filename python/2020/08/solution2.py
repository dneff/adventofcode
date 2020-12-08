
def printSolution(x):
    print(f"The solution is: {x}")


class Merlin:
    """a handheld game console"""

    def __init__(self, data):
        self.accumulator = 0
        self.pointer = 0
        self.history = []
        self.instructions = data

        self.boot_load()

    def boot_load(self):
        """can't trust the data in instructions
        so leveraging an auto-healer."""

        for instructions in self.auto_healer():
            self.reset()
            self_test = True
            while self_test:
                self.history.append(self.pointer)
                inst = instructions[self.pointer]
                self.process_instruction(inst)
                if self.pointer >= len(instructions):
                    return
                self_test = self.pointer not in self.history

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

    def reset(self):
        self.accumulator = 0
        self.pointer = 0
        self.history = []

    def auto_healer(self):
        """iterate through permutations of corrected instructions"""

        yield self.instructions
        healed = self.instructions.copy()
        jmps = [i for i, v in enumerate(self.instructions) if v[0] == "jmp"]
        for bad_inst in jmps:
            healed[bad_inst][0] = "nop"
            yield healed
            healed[bad_inst][0] = "jmp"

        nops = [i for i, v in enumerate(self.instructions) if v[0] == "nop"]
        for bad_inst in nops:
            healed[bad_inst][0] = "jmp"
            yield healed
            healed[bad_inst][0] = "nop"

        raise Exception("all instruction permutations tested.")


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