def print_solution(x):
    """prints solution"""
    print(f"The solution is: {x}")

def is_safe(levels):
    """checks if levels are safe"""

    if levels[0] == levels[1]:
        return False
    if levels[0] < levels[1]:
        for i in range(1, len(levels)):
            if levels[i] - levels[i - 1] > 3 or levels[i] - levels[i - 1] <= 0:
                return False
    else:
        for i in range(1, len(levels)):
            if levels[i - 1] - levels[i] > 3 or levels[i - 1] - levels[i] <= 0:
                return False

    return True

def check_unsafe_levels(levels):
    """try removing elements from levels to make them safe"""
    for i in range(0, len(levels)):
        if is_safe(levels[:i] + levels[i + 1:]):
            return True
    return False



def main():
    """finds solution"""
    filename = "./python/2024/input/02.txt"
    input_data = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f.readlines():
            numbers = [int(x) for x in line.split()]
            input_data.append(numbers)

    safe_levels = []
    unsafe_levels = []
    for levels in input_data:
        if is_safe(levels):
            safe_levels.append(levels)
        elif check_unsafe_levels(levels):
            safe_levels.append(levels)
        else:
            print(f"Unsafe levels: {levels}")
            unsafe_levels.append(levels)
    

    print_solution(len(safe_levels))



if __name__ == "__main__":
    main()
