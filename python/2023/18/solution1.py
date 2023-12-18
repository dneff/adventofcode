"""solves for 2023 day 18 solution 1"""

U, D, L, R = (0, -1), (0, 1), (-1, 0), (1, 0)


def print_solution(x):
    """prints the solution"""
    print(f"Solution: {x}")


def is_edge(pos, edges):
    """is position next to edge?"""
    x, y = pos
    possible = [(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]
    for loc in possible:
        if loc in edges:
            return True
    return False


def main():
    """solve the problem"""
    filename = "./python/2023/input/18.txt"
    instructions = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            direction, distance, color = line.strip().split(" ")
            instructions.append((direction, int(distance), color))

    min_x, min_y = 0, 0
    max_x, max_y = 0, 0
    x, y = 0, 0
    grid = {}
    grid[(x, y)] = "#000000"
    left_side = set()
    right_side = set()
    for direction, distance, color in instructions:
        offset = None
        left = None
        right = None
        if direction == "U":
            offset = U
            left = L
            right = R
        elif direction == "D":
            offset = D
            left = R
            right = L
        elif direction == "L":
            offset = L
            left = D
            right = U
        elif direction == "R":
            offset = R
            left = U
            right = D
        else:
            raise Exception(f"Unknown direction: {direction}")
        
        for _ in range(distance):

            x_left = x + left[0]
            y_left = y + left[1]
            left_side.add((x_left, y_left))

            x_right = x + right[0]
            y_right = y + right[1]
            right_side.add((x_right, y_right))

            x += offset[0]
            y += offset[1]
            grid[(x, y)] = color[1:-1]

            x_left = x + left[0]
            y_left = y + left[1]
            left_side.add((x_left, y_left))

            x_right = x + right[0]
            y_right = y + right[1]
            right_side.add((x_right, y_right))

            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)

    for y in range(min_y, max_y + 1):
        row = ""
        for x in range(min_x, max_x + 1):
            if (x, y) in grid:
                row += "X"
            else:
                row += "."

    if len(left_side) < len(right_side):
        inside = left_side
        outside = right_side
    else:
        inside = right_side
        outside = left_side

    for y in range(min_y, max_y + 1):
        row = ""
        for x in range(min_x, max_x + 1):
            if (x, y) in grid:
                row += "X"
            elif (x, y) in inside:
                row += "I"
            elif (x, y) in outside:
                row += " "
            else:
                if len(row) != 0 and row[-1] == "I":
                    row += "I"
                    inside.add((x, y))
                else:
                    row += " "


    # 43734 too high
    # 41355
    lagoon = set(grid).union(inside)
    print_solution(len(lagoon))

if __name__ == "__main__":
    main()
