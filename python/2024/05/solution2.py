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

def sort_update(update, rules):
    """sorts pages in an update according to rules"""
    sorted_update = []
    for page in update:
        if len(sorted_update) == 0:
            sorted_update.append(page)
        else:
            """try inserting page at every index. if the sorted_update is a valid update, use it"""
            for idx in range(len(sorted_update)):
                if valid_update(sorted_update[:idx] + [page] + sorted_update[idx:], rules):
                    sorted_update.insert(idx, page)
                    break
            if page not in sorted_update:
                sorted_update.append(page)
    return sorted_update


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

    invalid_updates = []

    for update in updates:
        if valid_update(update, rules):
            continue
        else:
            invalid_updates.append(update)

    middle_pages = []
    for update in invalid_updates:
        sorted_update = sort_update(update, rules)
        middle_pages.append(get_middle_page(sorted_update))
    
    print_solution(sum(middle_pages))

if __name__ == "__main__":
    main()
