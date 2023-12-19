"""solves for 2023 day 18 solution 2"""
import numpy as np


U, D, L, R = (0, -1), (0, 1), (-1, 0), (1, 0)

direction_converter = ["R", "D", "L", "U"]

def print_solution(x):
    """prints the solution"""
    print(f"Solution: {x}")


def shoelace(locs):
    shoelace = 0
    for i in range(len(locs) - 1):
        loc1 = locs[i]
        loc2 = locs[i + 1]
        shoelace += loc1[0] * loc2[1] -  loc2[0] * loc1[1]
    return abs(shoelace) // 2

    return area

def main():
    """solve the problem"""
    filename = "./python/2023/input/18.txt"
    instructions = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            direction, distance, color = line.strip().split(" ")
            instructions.append((direction, int(distance), color[2:-1]))

    updated_instructions = []
    for _,_,color in instructions:
        distance = int(color[:5],16)
        direction = direction_converter[int(color[-1], 10)]
        updated_instructions.append((direction, distance))

    x, y = 0, 0
    vertexes = [(x, y)]
    length = 0
    for direction, distance in updated_instructions:
        offset = None
        if direction == "U":
            offset = U
        elif direction == "D":
            offset = D
        elif direction == "L":
            offset = L
        elif direction == "R":
            offset = R
        else:
            raise Exception(f"Unknown direction: {direction}")
        
        x += offset[0] * distance
        y += offset[1] * distance
        length += abs(distance)
        vertexes.append((x, y))

    print_solution(shoelace(vertexes) + length//2 + 1)

if __name__ == "__main__":
    main()
