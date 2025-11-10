import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2019/8/input')


def solve_part1():
    content = AoCInput.read_file(INPUT_FILE).strip()

    step = 25 * 6
    parts = [content[i:i+step] for i in range(0, len(content), step)]

    check = {}

    for layer in parts:
        z = layer.count('0')
        c = layer.count('1') * layer.count('2')
        check[z] = c

    return check[min(check.keys())]


def solve_part2():
    content = AoCInput.read_file(INPUT_FILE).strip()

    step = 25 * 6
    parts = [content[i:i+step] for i in range(0, len(content), step)]

    image = []
    for i in range(len(parts[0])):
        for l in range(len(parts)):
            pixel = parts[l][i]
            if pixel != '2':
                if pixel == '0':
                    image.append(' ')
                else:
                    image.append('*')
                break

    result = []
    result.append("The image is:")
    for x in range(0, len(image), step):
        c = ''.join(image[x:x+step])
        for y in range(0, 25*6, 25):
            result.append(c[y:y+25])

    return '\n'.join(result)


answer1 = solve_part1()
AoCUtils.print_solution(1, answer1)

answer2 = solve_part2()
print(answer2)