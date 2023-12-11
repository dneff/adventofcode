"""solves 2023 day 11 part 1"""

from collections import defaultdict

def print_solution(x):
    """prints solution"""
    print(f"The solution is: {x}")


def expand(galaxy):
    """add empty row and column in empty locations"""
    expanded = []
    # expand rows
    for row in galaxy:
        expanded.append(row)
        if len(set(row[:])) == 1:
            expanded.append(row)
    # expand columns
    new_cols = []
    for idx in range(len(galaxy[0])):
        column = [row[idx] for row in galaxy]
        if len(set(column[:])) == 1:
            new_cols.append(idx)
    new_cols = sorted(new_cols, reverse=True)
    result = []
    for row in expanded:
        for col in new_cols:
            row = row[:col] + '.' + row[col:]
        result.append(row)
    return result
    
def main():
    """loads and solves puzzle"""
    filename = "./python/2023/input/11-test.txt"
    lines = []
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]
    
    expanded = expand(lines)    

    
if __name__ == "__main__":
    main()