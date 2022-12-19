def printSolution(x):
    print(f"The solution is: {x}")


def main():

    file = open("input.txt", "r")

    original = []
    reencoded = []

    for line in file:
        original.append(line.strip())

        encoded = line.strip()
        encoded = encoded.encode("ascii", "backslashreplace").replace(b"\\", b"\\\\").replace(b'"', b'\\"')
        encoded = b'"' + encoded + b'"'
        reencoded.append(encoded)

    diff = [len(x) - len(y) for x, y in zip(reencoded, original)]

    printSolution(sum(diff))


if __name__ == "__main__":
    main()
