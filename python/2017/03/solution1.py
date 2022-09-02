
def printSolution(x):
    print(f"The solution is: {x}")


def main():
    input = 347991
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    current_dir = 0
    x, y = 0, 0
    location_value = 1
    locations = {}

    locations[(x, y)] = location_value
    location_value +=1

    x, y = x + directions[current_dir][0], y + directions[current_dir][1]
    locations[(x, y)] = location_value
    current_dir += 1

    while location_value <= input:
        # should spiral turn?
        location_value += 1
        next_dir = (current_dir + 1) % 4
        next_loc = (x + directions[next_dir][0], y + directions[next_dir][1])
        if next_loc not in locations.keys():
            current_dir = next_dir
        next_loc = (x + directions[current_dir][0], y + directions[current_dir][1])
        x, y = next_loc
        locations[next_loc] = location_value

    # subtract one as we want MOVES count, not locations count
    printSolution(abs(x)+abs(y) - 1)

if __name__ == "__main__":
    main()