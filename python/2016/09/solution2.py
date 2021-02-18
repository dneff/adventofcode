def printSolution(x):
    print(f"The solution is: {x}")


def decompress(s):
    result = ''
    index = 0

    while index < len(s):
        if s[index] != '(':
            next_marker = s[index:].find('(')
            if next_marker >= 0:
                result += s[index:next_marker]
                index = next_marker - 1
            else:
                result += s[index:]
                index += len(s)
        else:
            index += 1
            end_marker = index + s[index:].find(')')
            marker = s[index:end_marker]
            characters, repeat = [int(x) for x in marker.split('x')]
            index = end_marker + 1
            result += s[index:index+characters] * repeat
            index += characters - 1
        index += 1
        print(len(s), index)

    return result


def decompress_v2(s):
    s = decompress(s)
    while '(' in s:
        print(len(s))
        s = decompress(s)
    return s

def main():
    file = open("input.txt", "r")

    data = file.readlines()[0]

    for x in ['(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN','X(8x2)(3x3)ABCY', '(27x12)(20x12)(13x14)(7x10)(1x12)A', '(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN']:
        result = decompress_v2(x)
        print(x, len(result))



   # printSolution(len(decompress(data)))

if __name__ == "__main__":
    main()