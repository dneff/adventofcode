def print_solution(x: int) -> None:
    """Print the solution with formatted output.

    Args:
        x (int): The solution value to print
    """
    print(f"The solution is: {x}")


def print_robots(robots: list[tuple[tuple[int, int], tuple[int, int]]]) -> None:
    """Print the robots in a grid format.

    Args:
        robots (list[tuple[tuple[int, int], tuple[int, int]]]): List of robots, where each robot is
            represented as ((x, y), (vx, vy)) containing position and velocity
    """
    min_x, max_x = min(robot[0][0] for robot in robots), max(
        robot[0][0] for robot in robots
    )
    min_y, max_y = min(robot[0][1] for robot in robots), max(
        robot[0][1] for robot in robots
    )
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (x, y) in [robot[0] for robot in robots]:
                print("#", end="")
            else:
                print(".", end="")
        print()


def get_adjacent_robots(
    robots: list[tuple[tuple[int, int], tuple[int, int]]], max_position: tuple[int, int]
) -> list[int]:
    """Calculate the number of adjacent robots in each row.

    Args:
        robots: List of robots, where each robot is ((x, y), (vx, vy))
        max_position (tuple[int, int]): Maximum x,y coordinates of the grid

    Returns:
        list[int]: List containing the maximum number of adjacent robots for each row
    """
    adjacent_robots = []
    for y in range(max_position[1]):
        x_pos = [robot[0][0] for robot in robots if robot[0][1] == y]
        x_pos.sort()
        gaps = [x_pos[i + 1] - x_pos[i] for i in range(len(x_pos) - 1)]
        # if the gap is 1, then the robots are adjacent
        # look for consecutive gaps of 1
        max_adjacent = 0
        current_adjacent = 0
        for gap in gaps:
            if gap == 1:
                current_adjacent += 1
            else:
                max_adjacent = max(max_adjacent, current_adjacent)
                current_adjacent = 0
        adjacent_robots.append(max_adjacent)
    return adjacent_robots


def move_robot(
    robot: tuple[int, int],
    velocity: tuple[int, int],
    max_position: tuple[int, int],
    turns: int,
) -> tuple[int, int]:
    """Move a robot by its velocity for a specified number of turns.

    Args:
        robot (tuple[int, int]): Current (x, y) position of the robot
        velocity (tuple[int, int]): (vx, vy) velocity vector
        max_position (tuple[int, int]): Maximum (x, y) coordinates of the grid
        turns (int): Number of turns to move the robot

    Returns:
        tuple[int, int]: New position of the robot after movement and wrapping
    """
    new_position = (robot[0] + velocity[0] * turns, robot[1] + velocity[1] * turns)
    new_position = new_position[0] % max_position[0], new_position[1] % max_position[1]
    return new_position


def main() -> None:
    """Process robot movement simulation to find Christmas tree formation.

    Reads robot positions and velocities from an input file and simulates their
    movement until they form a pattern resembling a Christmas tree. A Christmas
    tree formation is assumed when robots align vertically with sufficient density
    (10 or more adjacent robots in any row).

    Input file format:
        Each line contains position and velocity in format: p=x,y v=vx,vy
    """
    max_position = (101, 103)
    robots = []

    filename = "./python/2024/input/14.txt"
    with open(filename, "r", encoding="utf-8") as f:
        for line in f.readlines():
            p, v = line.strip().split(" ")
            p = tuple(int(x) for x in p.split("p=")[1].split(","))
            v = tuple(int(x) for x in v.split("v=")[1].split(","))
            robots.append((p, v))

    moving = True
    moved_robots = []
    seconds = 0
    density_frequency = {}
    while moving:
        for robot in robots:
            moved_pos = move_robot(robot[0], robot[1], max_position, 1)
            moved_robots.append((moved_pos, robot[1]))
        robots = moved_robots.copy()
        moved_robots = []
        seconds += 1

        adjacent_robots = get_adjacent_robots(robots, max_position)
        # just guessing that 10 is a good threshold
        if max(adjacent_robots) >= 10:
            moving = False
            break
    print_robots(robots)
    print_solution(seconds)


if __name__ == "__main__":
    main()
