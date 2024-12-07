def print_solution(x):
    """prints solution"""
    print(f"The solution is: {x}")


def main():
    """finds solution"""
    rules = []
    updates = []
    filename = "./python/2024/input/05-test.txt"
    with open(filename, "r", encoding="utf-8") as f:
        parsing_rules = True
        for line in f.readlines():
            if len(line.strip()) == 0:
                parsing_rules = False
                continue
            if parsing_rules:
                first, second = [int(x) for x in line.strip().split("|")]
                rules.append((first, second))
            else:
                updates.append([int(x) for x in line.strip().split(",")])

    print(f"Rules: {rules}")


if __name__ == "__main__":
    main()
