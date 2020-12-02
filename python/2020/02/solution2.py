def printSolution(x):
    print(f"The solution is: {x}")

def isValidPassword(policy, password):
    '''policy: test that character is in exactly one of two positions in password'''
    password = password.strip()
    positions, letter =  policy.strip().split(" ")
    pos1, pos2 = [int(x)-1 for x in positions.strip().split('-')]

    return [password[pos1], password[pos2]].count(letter) == 1

    
def main():
    file = open('input.txt', 'r')

    solution = [isValidPassword(*line.split(':')) for line in file]

    printSolution(solution.count(True))

if __name__ == "__main__":
    main()