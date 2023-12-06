"""solvers for day 6 solution 1"""
def print_solution(x):
    """prints the solution"""
    print(f"Solution: {x}")

def main():
    """solve the problem"""
    filename = "./input/06.txt"
    with open(filename, "r", encoding="utf-8") as f:
        time = f.readline().strip().split(':')[1]
        distance = f.readline().strip().split(':')[1]
    time = int(''.join(time.split()))
    distance = int(''.join(distance.split()))

    wins = 0
    winning = False

    for elapsed in range(1, time + 1):
        remaining = time - elapsed
        distance_traveled = elapsed * remaining
        if distance_traveled >= distance:
            winning = True
            wins += 1
        elif winning == True:
            break
            
    print_solution(wins)

if __name__ == "__main__":
    main()
