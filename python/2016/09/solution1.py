def printSolution(x):
    print(f"The solution is: {x}")


def decompress(s):
    result = 0
    index = 0

    while index < len(s):
        if s[index] != '(':
            result += 1
        else:
            index += 1
            end_marker = index + s[index:].find(')')
            marker = s[index:end_marker]
            characters, repeat = [int(x) for x in marker.split('x')]
            index = end_marker + 1
            substring = s[index:index+characters]
            result += len(substring) * repeat
            index += characters - 1
        index += 1

    return result

def main():
    file = open("input.txt", "r")

    for data in file.readlines():
        printSolution(decompress(data.strip()))


if __name__ == "__main__":
    main()
