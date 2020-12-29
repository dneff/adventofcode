from hashlib import md5


def printSolution(x):
    print(f"The solution is: {x}")


def main():
    input = "ckczppom"
    suffix = 0
    checking = True

    while checking:
        possible = input + str(suffix)
        possible_encoded = md5(possible.encode("utf-8")).hexdigest()
        if possible_encoded[:6] == "000000":
            print(possible_encoded)
            checking = False
            continue
        suffix += 1
    printSolution(suffix)


if __name__ == "__main__":
    main()
