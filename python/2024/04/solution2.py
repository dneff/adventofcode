def print_solution(x):
    print(f"The solution is: {x}")

def check_grid(grid):
    """check the diagonals of a 3x3 grid that all elements are different"""
    return len(set([grid[0][0], grid[1][1], grid[2][2]])) == 3 and len(set([grid[0][2], grid[1][1], grid[2][0]])) == 3


def main():
    """finds solution"""
    left, right = [], []
    filename = "./python/2024/input/04.txt"
    puzzle = {}
    max_x, max_y = 0, 0
    with open(filename, "r", encoding="utf-8") as f:
        for y,line in enumerate(f.readlines()):
            max_y = max(max_y, y)
            for x,cell in enumerate(line.strip()):
                puzzle[(x,y)] = cell
                max_x = max(max_x, x)

    xmas_count = 0
    for x in range(1, max_x):
        for y in range(1, max_y):
            if puzzle[(x,y)] == "A":
                # if X in corners, we can skip
                if 'X' in [puzzle[(x-1,y-1)], puzzle[(x+1,y-1)] ,puzzle[(x-1,y+1)], puzzle[(x+1,y+1)]]:
                    continue
                if check_grid([[puzzle[(x-1,y-1)], puzzle[(x,y-1)], puzzle[(x+1,y-1)]],
                               [puzzle[(x-1,y)], puzzle[(x,y)], puzzle[(x+1,y)]],
                               [puzzle[(x-1,y+1)], puzzle[(x,y+1)], puzzle[(x+1,y+1)]]]):
                    xmas_count += 1

    print_solution(xmas_count)


if __name__ == "__main__":
    main()
