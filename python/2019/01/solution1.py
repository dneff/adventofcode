import math

def moduleFuel(mass):
    return (mass // 3) - 2

def main():
    result = 0

    file = open('input1.txt', 'r')

    for line in file:
        result += moduleFuel(int(line.strip()))

    print(result)

if __name__ == "__main__":
    main()
