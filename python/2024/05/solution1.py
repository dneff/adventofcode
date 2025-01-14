def print_solution(x):
    """prints solution"""
    print(f"The solution is: {x}")

def valid_update(update, rules):
    """checks if an update is valid"""
    for idx, page in enumerate(update):
        if page in rules:
            if set(update[:idx]).intersection(rules[page]):
                return False
    return True

def get_middle_page(update):
    """gets the middle page of an update"""
    return update[len(update) // 2]

def main():
    """finds solution"""
    rules = {}
    updates = []
    filename = "./python/2024/input/05.txt"
    with open(filename, "r", encoding="utf-8") as f:
        parsing_rules = True
        for line in f.readlines():
            if len(line.strip()) == 0:
                parsing_rules = False
                continue
            if parsing_rules:
                first, second = [int(x) for x in line.strip().split("|")]
                if first not in rules:
                    rules[first] = []
                rules[first].append(second)
            else:
                updates.append([int(x) for x in line.strip().split(",")])

    valid_updates = []

    for update in updates:
        if valid_update(update, rules):
            valid_updates.append(get_middle_page(update))

    print_solution(sum(valid_updates))

if __name__ == "__main__":
    main()
