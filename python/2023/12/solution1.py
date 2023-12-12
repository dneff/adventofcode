"""solves 2023 day 12 part 1"""

def print_solution(x):
    """prints solution"""
    print(f"The solution is: {x}")

def main():
    """main"""
    lines = []
    filename = "./python/2023/input/12-test.txt"
    with open(filename, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file.readlines()]

    print(lines)

if __name__ == "__main__":
    main()
