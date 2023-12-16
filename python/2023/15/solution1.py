"""solves for day 15, 2023 part 1"""

def print_solution(x):
    """prints solution"""
    print(f"The solution is: {x}")

def hash(s):
    """returns ascii value of x"""
    value = 0
    for c in s:
         value += ord(c)
         value *= 17
         value = value % 256
    return value

def main():
    """load puzzle and solve"""
    filename = "./python/2023/input/15.txt"
    lines = []
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readline().split(",")

    hashes = []
    for line in lines:
        hashes.append(hash(line))
    
    print_solution(sum(hashes))


if __name__ == "__main__":
    main()
