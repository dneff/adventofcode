import IntCode


def main():
    with open('input1.txt', 'r') as file:
        program = file.read().strip()

    comp = IntCode.IntCode(program)
    comp.push(1)
    comp.run()

    print(f"Part 1 solution is: {comp.output.pop()}")

    comp2 = IntCode.IntCode(program)
    comp2.push(5)
    comp2.run()
    print(f"Part 2 solution is: {comp2.pop()}")

if __name__ == "__main__":
    main()
