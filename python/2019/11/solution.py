from itertools import permutations
from IntCode import IntCode, InputInterrupt, OutputInterrupt
from collections import defaultdict


def newOrientation(orientation, turn):
    if turn == 0:
        orientation = (orientation - 1) % 4
    elif turn == 1:
        orientation = (orientation + 1) % 4

    return orientation

def newLocation(loc, direction):
    move = {
        'N': (0, 1),
        'E': (1, 0),
        'S': (0, -1),
        'W': (-1, 0)
    }    

    delta = move[direction]
    return loc[0] + delta[0], loc[1] + delta[1]         


def main():
    with open('input1.txt', 'r') as file:
        program = file.read().strip()

    panels = defaultdict(int)
    x, y = 0, 0
    panels[(x,y)] = 0

    direction = ['N', 'E', 'S', 'W']
    orientation = 0
    turn = False

    comp1 = IntCode(program)
    comp1.push(panels[(x, y)])

    painted = 0
    painted_panels = []

    while not comp1.complete:
        try:
            comp1.run()
        except(InputInterrupt):
                input = panels[(x, y)]
                comp1.push(input)
        except(OutputInterrupt):
            out = comp1.pop()

            if turn:
                orientation = newOrientation(orientation, out)
                x, y = newLocation((x, y), direction[orientation])
            else:
                if out == 1 and panels[(x, y)] == 0 and (x, y) not in painted_panels:
                    painted += 1
                    painted_panels.append((x, y))
                panels[(x,y)] = out
            turn = not turn

    print(f"Solution 1: {painted} panels are painted at least once.")

# -=-=-=- Part 2
    panels = defaultdict(int)
    x, y = 0, 5
    panels[(x,y)] = 1

    direction = ['N', 'E', 'S', 'W']
    orientation = 0
    turn = False

    comp2 = IntCode(program)
    comp2.push(panels[(x, y)])

    while not comp2.complete:
        try:
            comp2.run()
        except(InputInterrupt):
                input = panels[(x, y)]
                comp2.push(input)
        except(OutputInterrupt):
            out = comp2.pop()

            if turn:
                orientation = newOrientation(orientation, out)
                x, y = newLocation((x, y), direction[orientation])
            else:
                panels[(x,y)] = out
            turn = not turn
    
    white_panels = [x for x in panels.keys() if panels[x] == 1]
    max_row = max([x[1] for x in white_panels])
    max_col = max([x[0] for x in white_panels])

    print("Solution 2 (registration identifier):")
    for r in range(max_row + 1, -1, -1):
        row = []
        for c in range(max_col + 1):
            if (c,r) in white_panels:
                row.append('*')
            else:
                row.append(' ')
        print(f"{''.join(row)}")
    
    


if __name__ == "__main__":
    main()
