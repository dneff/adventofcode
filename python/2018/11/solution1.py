
from collections import defaultdict

def printSolution(x):
    print(f"The solution is {x}")

def powerLevel(serial_num, pos):
    x,y = pos
    rack_id = x + 10
    power_level = rack_id * y
    power_level += serial_num
    power_level *= rack_id
    power_level = (power_level//100) % 10
    power_level -= 5

    return power_level

def getGridPower(grid, pos):
    x,y = pos
    positions = [(x,y), (x, y+1), (x, y+2), (x+1,y), (x+1, y+1), (x+1, y+2), (x+2,y), (x+2, y+1), (x+2, y+2)]
    return sum([grid[x] for x in positions])


def main():
    serial_num = 1133
    grid = defaultdict(dict)

    for x in range(1, 301):
        for y in range(1, 301):
            grid[(x,y)] = powerLevel(serial_num, (x,y))

    grid_power = defaultdict(int)

    for x in range(1, 300 - 1):
        for y in range(1, 300 - 1):
            grid_power[(x,y)] = getGridPower(grid, (x,y))

    best = max(grid_power.values())
    for k,v in grid_power.items():
        if v == best:
            printSolution(k)

if __name__ == "__main__":
    main()