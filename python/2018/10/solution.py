import re

def printSolution(x):
    print(f"The solution is {x}")

def main():
    test = 'test.txt'
    puzzle = 'input.txt'

    active = puzzle

    stars = {}

    file = open(active, 'r')
    for index, line in enumerate(file.readlines()):
        r = re.findall(r'\<(.*?)\>',line)
        pos,vel = [x.split(', ') for x in r]
        pos = [int(x) for x in pos]
        vel = [int(x) for x in vel]

        stars[index] = {'pos': pos, 'vel': vel}

    max_y = max([x['pos'][1] for x in stars.values()])
    min_y = min([x['pos'][1] for x in stars.values()])
    distance = abs(max_y - min_y)

    tracking = True
    counter = 0
    while tracking:
        for k in stars.keys():
            stars[k]['pos'] = [a+b for a,b in zip(stars[k]['pos'], stars[k]['vel'])]
        max_y = max([x['pos'][1] for x in stars.values()])
        min_y = min([x['pos'][1] for x in stars.values()])
        new_distance = abs(max_y - min_y)
        if new_distance > distance:
            tracking = False
        else:
            distance = new_distance
        counter += 1

    for k in stars.keys():
        stars[k]['pos'] = [a-b for a,b in zip(stars[k]['pos'], stars[k]['vel'])]

    counter -= 1
    positions = set([tuple(x['pos']) for x in stars.values()])

    min_x = min([v[0] for v in positions])
    max_x = max([v[0] for v in positions])
    min_y = min([v[1] for v in positions])
    max_y = max([v[1] for v in positions])

    for row in range(min_y, max_y + 1):
        output = ''
        for col in range(min_x, max_x + 1):
            if (col, row) in positions:
                output += '#'
            else:
                output += ' '
        print(output)

    printSolution(counter)
    

if __name__ == "__main__":
    main()