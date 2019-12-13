


def hasPair(number):
    digits = ['?'] + [x for x in str(number)] + ['?']
    for index in range(1,6):
        if  digits[index] == digits[index + 1] and \
            digits[index] != digits[index - 1] and \
            digits[index + 1] != digits[index + 2]:
                return True

    return False


def isOrdered(number):
    digits = [int(x) for x in str(number)]
    return digits == sorted(digits)

def main():
    count = 0
    start, end = 158126, 624574
    for number in range(158126, 624574):
        if hasPair(number) and isOrdered(number):
            count += 1
    print(f"The solution is: {count}")

if __name__ == "__main__":
    main()