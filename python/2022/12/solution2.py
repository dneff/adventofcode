from string import ascii_lowercase
from collections import deque

def print_solution(x):
    """print any value passed in"""
    print(f"The solution is {x}")


def get_adjacent(pos, grid):
    """
    get_adjacent: finds valid next positions in grid
    returns list of positions
    """
    possible = [
        (pos[0] + 1,pos[1]),
        (pos[0] - 1,pos[1]),
        (pos[0],pos[1] + 1),
        (pos[0],pos[1] - 1)
        ]
    return [x for x in possible if x in grid]

def breadth_search(start, end, grid):
    """
    breadth_search: a BFS search, return length of shortest downhill path
    """
    heights = {c: ord(c) for c in ascii_lowercase}
    heights["S"] = ord("a")
    heights["E"] = ord("z")

    queue, seen = deque(), set()
    queue.append([start])

    while queue:
        path = queue.popleft()
        x, y = path[-1]
        current_height = heights[grid[(x,y)]]

        if (x, y) not in seen:
            seen.add((x, y))
            if heights[grid[(x,y)]] == heights[grid[end]]:
                return len(path) - 1
            
            for location in get_adjacent((x,y), grid):
                location_height = heights[grid[location]]
                if current_height - location_height <= 1:
                    new_path = path[:]
                    new_path.append(location)
                    queue.append(new_path)

def main():
    grid = {}
    start = ()
    end = ()
    with open("../input/12-test.txt", "r", encoding="utf-8") as f:
        for y, line in enumerate(f):
            for x, char in enumerate(line.strip()):
                grid[(x,y)] = char
                if char == "S":
                    start = (x,y)
                if char == "E":
                    end = (x,y)

    print_solution(breadth_search(end, start, grid))


if __name__ == "__main__":
    main()
