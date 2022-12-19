import math

def moduleFuel(mass):
    result = 0
    fuel = (mass // 3) - 2
    while fuel > 0:
        result += fuel
        fuel = (fuel // 3) - 2
    return result


def main():
    result = 0

    file = open('input1.txt', 'r')

    for line in file:
        result += moduleFuel(int(line.strip()))

    print(result)

if __name__ == "__main__":
    main()
