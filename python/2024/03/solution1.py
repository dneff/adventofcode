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
        for line in f.readlines():
            instructions.extend(find_instructions(line))

    values = [calculate_instructions(instruction) for instruction in instructions]
    print_solution(sum(values))


if __name__ == "__main__":
    main()
