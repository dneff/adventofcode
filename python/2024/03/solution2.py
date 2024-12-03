import re


def print_solution(x):
    """prints solution"""
    print(f"The solution is: {x}")


def find_instructions(memory):
    """find valid instructions which are formatted as 'mul(integer, integer)'
    and returns a list of them"""
    return re.findall(r"mul\(\d+,\d+\)", memory)


def calculate_instructions(instruction):
    """calculates the multiplication of two integers"""
    x, y = instruction.split("(")[1].split(")")[0].split(",")
    return int(x) * int(y)


def main():
    """finds solution"""
    filename = "./python/2024/input/03.txt"
    input_data = []

    with open(filename, "r", encoding="utf-8") as f:
        instructions = []
        enabled = True
        lines = list(f.readlines())
        line = "".join(lines)
        for idx in range(len(line)):
            if line[idx:].startswith("don't()"):
                enabled = False
            elif line[idx:].startswith("do()"):
                enabled = True
            elif line[idx:].startswith("mul(") and enabled:
                # grab the next 12 characters and find instruction
                instructions.extend(find_instructions(line[idx : idx + 12]))
        values = [calculate_instructions(instruction) for instruction in instructions]
        print_solution(sum(values))


if __name__ == "__main__":
    main()
