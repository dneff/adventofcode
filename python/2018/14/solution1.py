
def printSolution(x):
    print(f"The solution is {x}")

def main():
    test = [int(x) for x in '37']

    active = test

    trials = int('047801')
    current = 0

    chef_a = 0
    chef_b = 1

    while current < (trials + 10):
        new_recipe = active[chef_a] + active[chef_b]
        active.extend([int(x) for x in str(new_recipe)])
        chef_a += active[chef_a] + 1
        chef_a = chef_a % len(active)
        chef_b += active[chef_b] + 1
        chef_b = chef_b % len(active)
        current += 1

    result = [str(x) for x in active[trials: trials + 10]]
    printSolution(''.join(result))

if __name__ == "__main__":
    main()