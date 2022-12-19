def printSolution(x):
    print(f"The solution is: {x}")

def isValidPassword(policy, password):
    '''policy: test that character count in password is between min/max'''

    counts, letter =  policy.strip().split(" ")
    minCount, maxCount = [int(x) for x in counts.strip().split('-')]

    return minCount <= password.count(letter) <= maxCount

def main():
    file = open('input.txt', 'r')

    solution = [isValidPassword(*line.split(':')) for line in file]

    printSolution(solution.count(True))

if __name__ == "__main__":
    main()