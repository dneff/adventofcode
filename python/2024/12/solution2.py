def print_solution(x: int) -> None:
    """Print the formatted solution.

    Args:
        x: The value to print
    """
    print(f"The solution is: {x}")


def is_adjacent(point1: tuple[int, int], point2: tuple[int, int]) -> bool:
    """Check if two points are adjacent (share a side).

    Args:
        point1: First point coordinates (x, y)
        point2: Second point coordinates (x, y)

    Returns:
        True if points are adjacent, False otherwise
    """
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1]) == 1


def find_plots(crop: list[tuple[int, int]]) -> list[list[tuple[int, int]]]:
    """Group coordinates into lists of adjacent coordinates using DFS.

    Args:
        crop: List of (x, y) coordinates representing crop positions

    Returns:
        List of plots, where each plot is a list of adjacent coordinates
    """
    positions = set(crop)  # Convert to set for O(1) lookups
    plots = []

    def dfs(start_pos):
        plot = []
        stack = [start_pos]
        while stack:
            pos = stack.pop()
            if pos in positions:
                plot.append(pos)
                positions.remove(pos)
                # Check all adjacent positions
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    next_pos = (pos[0] + dx, pos[1] + dy)
                    if next_pos in positions:
                        stack.append(next_pos)
        return plot

    while positions:
        start_position = next(iter(positions))  # Get any remaining position
        plot = dfs(start_position)
        plots.append(plot)

    return plots


def find_area(plot: list[tuple[int, int]]) -> int:
    """Calculate the area of a plot.

    Args:
        plot: List of (x, y) coordinates representing a plot

    Returns:
        Number of coordinates in the plot
    """
    return len(plot)


def find_perimeter(plot: list[tuple[int, int]]) -> int:
    """Calculate the perimeter of a plot.

    Args:
        plot: List of (x, y) coordinates representing a plot

    Returns:
        Length of the plot's perimeter (number of edges not adjacent to another plot coordinate)
    """
    perimeter = 0
    for point in plot:
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            next_point = (point[0] + dx, point[1] + dy)
            if next_point not in plot:
                perimeter += 1
    return perimeter


def find_sides(plot: list[tuple[int, int]]) -> int:
    """Find the number of sides of a plot.

    A side is defined as a continuous straight line of cells along the perimeter.

    Args:
        plot: List of (x, y) coordinates representing a plot

    Returns:
        Number of sides in the plot
    """
    plot_set = set(plot)
    sides = 0
    # Track both the cell and the direction of the edge
    visited = set()

    def get_continuous_side(x, y, dx, dy):
        """Get all cells that are part of the same continuous side."""
        side_cells = {(x, y)}
        # Check in both perpendicular directions
        for pdx, pdy in [(dy, dx), (-dy, -dx)]:
            nx, ny = x + pdx, y + pdy
            while (nx, ny) in plot_set and (nx + dx, ny + dy) not in plot_set:
                side_cells.add((nx, ny))
                nx, ny = nx + pdx, ny + pdy
        return side_cells

    for x, y in plot:
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if (x + dx, y + dy) not in plot_set:  # Found an edge
                if ((x, y), (dx, dy)) in visited:
                    continue

                # Get all cells that form this continuous side
                side_cells = get_continuous_side(x, y, dx, dy)

                # Mark all cells in this side as visited in this direction
                for cell in side_cells:
                    visited.add((cell, (dx, dy)))

                sides += 1

    return sides


def get_price(area: int, sides: int) -> int:
    """Calculate the price of a plot based on its area and perimeter.

    Args:
        area: The area of the plot
        sides: The number of sides of the plot

    Returns:
        The price (area * sides)
    """
    return area * sides


def main() -> None:
    """Process crop data from input file and analyze plots.

    Reads a grid of letters from file where each letter represents a crop type.
    For each crop type:
    1. Groups adjacent crops into plots
    2. Calculates area and perimeter of each plot
    3. Prints results

    Input file format:
        Grid of letters where each letter represents a crop type
        Example:
        ABC
        AAC
        BBC
    """
    crops = {}
    filename = "./python/2024/input/12.txt"
    with open(filename, "r", encoding="utf-8") as f:
        for y, line in enumerate(f.readlines()):
            for x, crop in enumerate(line.strip()):
                if crop not in crops:
                    crops[crop] = []
                crops[crop].append((x, y))

    # find total price for fencing all plots
    total_price = 0
    for crop in crops:
        print(f"{crop}:")
        for plot in find_plots(crops[crop]):
            area = find_area(plot)
            sides = find_sides(plot)
            print(
                f"\tarea:\t\t{area}\n\tsides:\t\t{sides}\n\tprice:\t\t{get_price(area, sides)}\n"
            )
            total_price += get_price(area, sides)
    print_solution(total_price)


if __name__ == "__main__":
    main()
