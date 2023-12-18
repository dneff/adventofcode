"""solves 2023 day 17 part 2"""
from collections import defaultdict
from heapq import heappush, heappop


def print_solution(x):
    """prints solution"""
    print(f"The solution is:{x}")


def get_straight(current_direction, direction, straight):
    """find manhattan distance between two points"""
    if (direction[0], direction[1]) == (-current_direction[0], -current_direction[1]):
        return None
    if direction == current_direction:
        return straight + 1
    if current_direction == (0, 0) or straight >= 4:
        return 1


def crooked_dijkstra(grid, start_loc):
    """
    find the path including path limitations

    """
    adjacent = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    q = [(0, start_loc, (0, 0), 1)]
    visited = defaultdict(lambda: defaultdict(lambda: float("inf")))

    while q:
        (cost, loc, direction, straight) = heappop(q)
        for new_direction in adjacent:
            new_straight = get_straight(direction, new_direction, straight)
            if not new_straight or new_straight == 11:
                continue
            new_loc = (loc[0] + new_direction[0], loc[1] + new_direction[1])
            if new_loc not in grid:
                continue
            new_cost = cost + grid[new_loc]
            if new_cost < visited[new_loc][direction, new_straight]:
                visited[new_loc][direction, new_straight] = new_cost
                heappush(q, (new_cost, new_loc, new_direction, new_straight))

    return visited


def main():
    """loads puzzle and solves"""
    lines = []
    filename = "./python/2023/input/17.txt"
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]

    max_x = len(lines[0]) - 1
    max_y = len(lines) - 1
    start = (0, 0)
    destination = (max_x, max_y)

    grid = {}
    for y, row in enumerate(lines):
        for x, loc in enumerate(row):
            grid[x, y] = int(loc)

    distances = crooked_dijkstra(grid, start)
    results = distances[destination]
    # need to end with straight > 4
    valid_costs = []
    for (direction, distance), cost in results.items():
        if distance >= 4:
            valid_costs.append(cost)

    print_solution(min(valid_costs))


if __name__ == "__main__":
    main()
