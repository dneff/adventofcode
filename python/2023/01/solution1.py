def printSolution(x):
    """Prints the solution"""
    print(f"The solution is: {x}")

def firstLastInt(string):
    """Returns the first and last integer in a string"""
    ints = [c for c in string if c.isdigit()]
    return int(''.join([ints[0], ints[-1]]))

def main():
    file = open("../input/01.txt", "r")
    lines = file.readlines()
    file.close()
    values = [firstLastInt(line.strip()) for line in lines]
    printSolution(sum(values))

    
if __name__ == "__main__":
    main()
