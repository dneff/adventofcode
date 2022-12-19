
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

def getGridPower(grid, pos, size):
    #uses summed-area grid
    x,y = pos
    x -= 1
    y -= 1
    nw = ne = sw = se = 0

    if x < 1 or y < 1:
        return 0

    if x+size > 300 or y+size > 300:
        return 0

    if (x,y) in grid.keys():
        nw = grid[(x, y)]

    if (x+size,y) in grid.keys():
        ne = grid[(x+size, y)]

    if (x,y+size) in grid.keys():
        sw = grid[(x, y+size)]

    if (x+size,y+size) in grid.keys():
        se = grid[(x+size, y+size)]

    return se - sw - ne + nw




def main():
    serial_num = 1133
    grid = defaultdict(dict)

    for x in range(1, 301):
        for y in range(1, 301):
            grid[(x,y)] = powerLevel(serial_num, (x,y))

    
    sum_table = defaultdict(int)
    sum_table[(1, 1)] = grid[(1, 1)]

    for x in range(3, 301):
        for y in range(3, 301):
            value = grid[(x,y)]
            if x > 2:
                value += sum_table[(x-1,y)]
            if y > 2:
                value += sum_table[(x, y-1)]
            value -= sum_table[(x-1, y-1)]
            sum_table[(x,y)] = value

    optimal_size = defaultdict(list)

    for energy_size in range(1, 301):
        max_energy = -999999
        max_loc = (0,0)
        for eg_x in range(1, 302 - energy_size):
            for eg_y in range(1, 302 - energy_size):
                energy = getGridPower(sum_table, (eg_x, eg_y), energy_size)
                if energy > max_energy:
                    max_energy = energy
                    max_loc = (eg_x, eg_y)

        optimal_size[energy_size] = (max_energy, max_loc, energy_size)

    best = max(optimal_size.values())
    printSolution(best[1:])
 
if __name__ == "__main__":
    main()