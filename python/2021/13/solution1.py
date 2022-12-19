def printSolution(x):
    print(f"The solution is {x}")


def foldPaper(paper, instruction):
    direction, location = instruction
    folded = []
    if direction == 'y':
        folded = [points for points in paper.keys() if points[1] > location]
        for point in folded:
            offset = abs(point[1] - location)
            new_loc = (point[0], location - offset)
            paper.pop(point)
            paper[new_loc] = '#'
    else:
        folded = [points for points in paper.keys() if points[0] > location]
        for point in folded:
            offset = abs(point[0] - location)
            new_loc = (location - offset, point[1])
            paper.pop(point)
            paper[new_loc] = '#'


def printPaper(paper):
    max_x = max([p[0] for p in paper.keys()])
    max_y = max([p[1] for p in paper.keys()])

    for y in range(max_y + 1):
        row = ''
        for x in range(max_x + 1):
            if (x, y) in paper:
                row += '#'
            else:
                row += ' '
        print(row)

def main():
    test = 'test.txt'
    puzzle = 'input.txt'

    paper = {}
    instructions = []

    file = open(puzzle, 'r')
    data = [line.strip() for line in file.readlines()]
 
    for line in data:
        if line:
            x, y = [int(x) for x in line.split(',')]
            paper[(x, y)] = '#'
        else:
            break

    for line in data[-1::-1]:
        if line:
            line = line.split()[-1]
            fold_dir, fold_loc = line.split('=')
            instructions.append((fold_dir, int(fold_loc)))
        else:
            break

    instructions = instructions[::-1]

    for i in instructions:
        foldPaper(paper, i)
        break

    printSolution(len(paper.keys()))


if __name__ == "__main__":
    main()
