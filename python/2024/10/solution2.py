def print_solution(x):
    print(f"The solution is: {x}")


def find_sequences(grid, starting_position, visited=None):
    """Recursively finds all possible sequences of consecutive numbers from a starting position.
    
    Args:
        grid (dict): Dictionary with (x,y) coordinates as keys and digit values as values
        starting_position (tuple): The (x,y) coordinates to start searching from
        visited (set): Set of positions already visited in current path
    
    Returns:
        list: all possible sequences found from this position
        
    A sequence is valid if it contains consecutive numbers (current value + 1)
    in adjacent cells (up, down, left, right). A complete sequence ends at 9.
    """
    if visited is None:
        visited = set()

    x, y = starting_position
    current_value = grid[x, y]

    # mark the current position as visited
    visited.add((x, y))

    ending_positions = []
    if current_value == 9:
        ending_positions.append((x, y))
        return ending_positions

    for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        nx, ny = x + dx, y + dy
        if (nx, ny) in grid and (nx, ny) not in visited and grid[nx, ny] == current_value + 1:
            ending_positions.extend(find_sequences(grid, (nx, ny), visited.copy()))
    return ending_positions


def main():
    """Finds all valid number sequences in a grid of digits.
    
    Reads a grid of single digits from a file where each line represents a row.
    Starting from each '0' in the grid, finds all possible sequences of consecutive
    numbers (0-9) by moving to adjacent cells (up, down, left, right).
    
    The grid is stored as a dictionary with (x,y) coordinates as keys and digit
    values as values. A sequence is valid if:
    - It starts with 0
    - Each next number is exactly one more than the previous
    - Numbers must be in adjacent cells (orthogonally connected)
    - The sequence ends at 9
    
    Returns:
        Prints the total count of all valid sequences found in the grid
    """
    grid = {}
    starting_positions = []
    filename = "./python/2024/input/10.txt"
    with open(filename, "r", encoding="utf-8") as f:
        for y, line in enumerate(f.readlines()):
            for x, digit in enumerate(line.strip()):
                grid[x, y] = int(digit)
                if digit == "0":
                    starting_positions.append((x, y))

    sequence_count = 0
    for starting_position in starting_positions:
        sequence_count += len(find_sequences(grid, starting_position))
    print_solution(sequence_count)


if __name__ == "__main__":
    main()
