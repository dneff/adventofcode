import re

numbers = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight':8,
    'nine': 9
    }

def printSolution(x):
    """Prints the solution"""
    print(f"The solution is: {x}")

def firstLastInt(string):
    """Returns the first and last integer in a string"""
    ints = [c for c in string if c.isdigit()]
    return int(''.join([ints[0], ints[-1]]))

def substituteDigit(string):
    """Substitutes the digit words for digits
    use regex to find the digit words"""
    print(string.strip())
    """regex = r"(?=(" + '|'.join(numbers.keys()) + r"))"
    print(regex)
    indexes = {match.start(): match.group() for match in re.finditer(regex, string) if match.group() in numbers.keys()}
    """
    indexes = {string.find(key): key for key in numbers if string.find(key) != -1}
    print(indexes)
    if len(indexes) == 0:
        return string
    minKey = indexes[min(indexes)]
    maxKey = indexes[max(indexes)]
    string = string.replace(minKey, str(numbers[minKey]))
    string = string.replace(maxKey, str(numbers[maxKey]))
    print(string)
    return string

def main():
    file = open("./input/01-test2.txt", "r")
    lines = file.readlines()
    file.close()

    lines = [substituteDigit(line) for line in lines]
    values = [firstLastInt(line.strip()) for line in lines]
    for x,y in zip(lines, values):
        print(f"{x.strip()} -> {y}")
    # 55712 high
    # 55686 low
    printSolution(sum(values))

    
if __name__ == "__main__":
    main()
