def print_solution(x):
    print(f"The solution is: {x}")

def resolve_entry(entry):
    """entry is two parts, first a target number, then a list of numbers"""
    target = entry[0]
    numbers = entry[1:]
    """the list of numbers can either be multiplied or added together in order"""
    """if the target number can be reached, return the number"""
    """if the target number cannot be reached, return 0"""
    results = [numbers.pop(0)]
    while numbers:
        value = numbers.pop(0)
        new_results = []
        for result in results:
            new_results.append(result * value)
            new_results.append(result + value)
        results = new_results

    if target in results:
        return target
    else:
        return 0

def main():
    """finds solution"""
    filename = "./python/2024/input/07.txt"
    with open(filename, "r", encoding="utf-8") as f:
        results = []
        for line in f.readlines():
            entry = [int(x) for x in line.strip().replace(":", "").split()]
            results.append(resolve_entry(entry))
        print_solution(sum(results))



if __name__ == "__main__":
    main()
