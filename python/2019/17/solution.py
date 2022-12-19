from IntCode import IntCode, InputInterrupt, OutputInterrupt
from collections import deque


def isIntersection(grid, x, y):
    check = [grid[y+1][x], grid[y-1][x], grid[y][x+1], grid[y][x-1], grid[y][x]]
    return all([x == '#' for x in check])


def main():
    with open('input1.txt', 'r') as file:
        program = file.read().strip()

    comp1 = IntCode(program)
    comp1.complete = False


    view = []
    while not comp1.complete:
        try:
            comp1.run()
        except OutputInterrupt:
            p = chr(int(comp1.pop()))
            view.append(p)

    grid = []
    for l in ''.join(view).strip().split('\n'):
        grid.append([x for x in l])

    intersections = []
    for y in range(1, len(grid) - 2):
        for x in range(1, len(grid[y]) - 1):
            if grid[y][x] == '#' and isIntersection(grid, x, y):
                intersections.append((x, y))

    print(f"Solution 1: The sum of the alignment parameters is: {sum([x*y for x, y in intersections])}")

# Part 2 -=-=-=-=-

    #print(f"{''.join(view)}")
    # solved this one by hand from printing out the above
    move_routine = "A,B,A,B,A,C,B,C,A,C\n"
    A = "L,6,R,12,L,6\n"
    B = "R,12,L,10,L,4,L,6\n"
    C = "L,10,L,10,L,4,L,6\n"
    video = "n\n"

    #print(f"{','.join([str(ord(x)) for x in A])}")
    
    comp2 = IntCode(program)
    comp2.complete = False
    comp2.memory[0] = 2

    for s in [move_routine, A, B, C, video]: 
        for c in s:
            comp2.push(ord(c))

    display = []
    while not comp2.complete:
        try:
            comp2.run()
        except OutputInterrupt:
            p = chr(int(comp2.pop()))
            display.append(p)

    print(f"Solution 2: The vacuum robot collected {ord(display[-1])} units of space dust.")

if __name__ == "__main__":
    main()