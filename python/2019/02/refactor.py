import IntCode


def main():
    with open('input1.txt', 'r') as file:
        program = file.read().strip()

    comp = IntCode.IntCode(program)
    comp.run()

    print(f"Part 1 solution is: {comp.memory[0]}")

    for noun in range(100):
        for verb in range(100):
            comp = IntCode.IntCode(program)
            comp.memory[1] = noun
            comp.memory[2] = verb
            comp.run()

            if comp.memory[0] == 19690720:
                print(f"Part 2 solution is: {100 * noun + verb}")
                break


if __name__ == "__main__":
    main()
