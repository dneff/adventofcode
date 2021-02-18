def printSolution(x):
    print(f"The solution is: {x}")


def decompress(s):
    result = ''
    index = 0

    while index < len(s):
        if s[index] != '(':
            result += s[index]
        else:
            index += 1
            end_marker = index + s[index:].find(')')
            marker = s[index:end_marker]
            characters, repeat = [int(x) for x in marker.split('x')]
            index = end_marker + 1
            result += s[index:index+characters] * repeat
            index += characters - 1
        index += 1

    return result


def main():
    file = open("input.txt", "r")

    data = file.readlines()[0]

    printSolution(len(decompress(data)))


if __name__ == "__main__":
    main()
