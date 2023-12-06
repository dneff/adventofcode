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
    time = [int(x) for x in time.split()]
    distance = [int(x) for x in distance.split()]

    winning_combos = []
    for t,d in zip(time, distance):
        wins = []
        for elapsed in range(1,t+1):
            remaining = t - elapsed
            distance_traveled = elapsed * remaining
            if distance_traveled > d:
                wins.append((elapsed, remaining))
        winning_combos.append(len(wins))
    
    score = 1
    for c in winning_combos:
        score *= c
    
    print_solution(score)

if __name__ == "__main__":
    main()
