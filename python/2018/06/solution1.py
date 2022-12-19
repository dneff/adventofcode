from collections import defaultdict

def printSolution(x):
    print(f"The solution is {x}")

def findDistance(a,b):
    return abs(b[0] - a[0]) + abs(b[1] - a[1])

def findClosest(point, nodes):
    distances = []
    for n in nodes:
        distances.append((n, findDistance(n, point)))
    distances.sort(key = lambda x: x[1])

    if distances[0][1] == distances[1][1]:
        return (-1,-1)
    else:
        return(distances[0][0])

def main():
    locations = []
    file = open('input.txt', 'r')
    for line in file:
        x, y = line.strip().split(', ')
        x, y = int(x), int(y)
        locations.append((x, y))

    loc_x = [x[0] for x in locations]
    min_x, max_x = min(loc_x), max(loc_x)

    loc_y = [x[1] for x in locations]
    min_y, max_y = min(loc_y), max(loc_y)

    borders = [(min_x, max_x), (min_y, max_y)]
    infinity_locations = set()
    for l in locations:
        if l[0] in borders[0] or l[1] in borders[1]:
            infinity_locations.add(l)
    
    # boarders have infinity locations
    for boarder_x in range(min_x - 10, max_x + 10):
        infinity_locations.add(findClosest((boarder_x, min_y - 10), locations))
        infinity_locations.add(findClosest((boarder_x, max_y + 10), locations))

    for boarder_y in range(min_y - 10, max_y + 10):
        infinity_locations.add(findClosest((min_x - 10, boarder_y), locations))
        infinity_locations.add(findClosest((max_x + 10, boarder_y), locations))

    areas = defaultdict(int)

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            owner = findClosest((x,y), locations)
            if owner not in infinity_locations:
                areas[owner] += 1
    
    for l in infinity_locations:
        if l in areas.keys():
            areas.pop(l)

    printSolution(max(areas.values()))


if __name__ == "__main__":
    main()