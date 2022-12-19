def printSolution(x):
    print(f"The solution is: {x}")


def getAdjacent(loc):
    offsets = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    adjacent = [(x[0]+loc[0], x[1]+loc[1]) for x in offsets]
    return adjacent


def main():
    input = 347991
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    current_dir = 0
    x, y = 0, 0
    locations = {}

    locations[(x, y)] = 1

    x, y = x + directions[current_dir][0], y + directions[current_dir][1]
    adj = getAdjacent((x, y))
    adj_values = []
    for point in adj:
        if point in locations.keys():
            adj_values.append(locations[point])
    locations[(x, y)] = sum(adj_values)
    current_dir += 1

    while locations[(x, y)] <= input:
        # should spiral turn?
        next_dir = (current_dir + 1) % 4
        next_loc = (x + directions[next_dir][0], y + directions[next_dir][1])
        if next_loc not in locations.keys():
            current_dir = next_dir
        next_loc = (x + directions[current_dir][0], y + directions[current_dir][1])
        x, y = next_loc
        adj = getAdjacent((x, y))
        adj_values = []
        for point in adj:
            if point in locations.keys():
                adj_values.append(locations[point])
        locations[(x, y)] = sum(adj_values)

    printSolution(locations[(x,y)])


if __name__ == "__main__":
    main()
