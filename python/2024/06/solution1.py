def print_solution(x):
    print(f"The solution is: {x}")


class Guard:
    def __init__(self, position, grid):
        self.marching = True
        self.position = position
        self.direction = 0
        self.grid = grid
        self.directions = ["N", "E", "S", "W"]
        self.direction_map = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}

    def move(self):
        new_position = (
            self.position[0] + self.direction_map[self.directions[self.direction]][0],
            self.position[1] + self.direction_map[self.directions[self.direction]][1],
        )
        if new_position not in self.grid:
            self.marching = False
        elif self.grid[new_position] == "#":
            self.direction = (self.direction + 1) % 4
        else:
            self.position = new_position


def main():
    """finds solution"""

    """load grid coordinates from file"""
    grid = {}
    guard_position = None
    filename = "./python/2024/input/06.txt"
    with open(filename, "r", encoding="utf-8") as f:
        for y, line in enumerate(f.readlines()):
            for x, char in enumerate(line.strip()):
                if char == "^":
                    guard_position = (x, y)
                    grid[(x, y)] = "."
                else:
                    grid[(x, y)] = char

    """find the number of unique positions the guard visits"""
    positions = set()
    positions.add(guard_position)

    guard = Guard(guard_position, grid)
    while guard.marching:
        guard.move()
        positions.add(guard.position)

    print_solution(len(positions))


if __name__ == "__main__":
    main()
