
def printSolution(x):
    print(f"The solution is {x}")

def main():
    file = open('input.txt', 'r')
    line_count = 0
    data = [int(x) for x in file.readline().strip()]
    line_count += 1
    for line in file.readlines():
        line_data = [int(x) for x in line.strip('\n')]
        data = [x+y for x,y in zip(data, line_data)]
        line_count += 1

    gamma = ''.join(["1" if x > line_count//2 else "0" for x in data])
    epsilon = ''.join(["1" if x < line_count//2 else "0" for x in data])


    printSolution(int(gamma, 2) * int(epsilon, 2))

if __name__ == "__main__":
    main()