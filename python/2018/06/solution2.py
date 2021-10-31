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

def inCluster(point, nodes):
    distances = []
    for n in nodes:
        distances.append(findDistance(n, point))
    return sum(distances) < 10000

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

    in_region = set()

    for x in range(min_x, max_x):
        for y in range(min_y, max_y):
            if inCluster((x,y), locations):
                in_region.add((x,y))

    printSolution(len(in_region))



if __name__ == "__main__":
    main()