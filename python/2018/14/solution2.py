
def printSolution(x):
    print(f"The solution is {x}")

def main():
    test = [int(x) for x in '37']

    active = test

    #sequence = '59414'
    sequence = '047801'
    current = 0

    chef_a = 0
    chef_b = 1
    current_sequence = ''
    while sequence not in current_sequence[-20:]:
        new_recipe = active[chef_a] + active[chef_b]
        active.extend([int(x) for x in str(new_recipe)])
        chef_a += active[chef_a] + 1
        chef_a = chef_a % len(active)
        chef_b += active[chef_b] + 1
        chef_b = chef_b % len(active)
        result = [str(x) for x in active[-20:]]
        current_sequence = ''.join(result)

    result = ''.join([str(x) for x in active])
    printSolution(len(result.split(sequence)[0]))

if __name__ == "__main__":
    main()