def print_solution(x):
    print(f"The solution is: {x}")


def get_safety_factor(
    robots: list[tuple[tuple[int, int], tuple[int, int]]], max_position: tuple[int, int]
) -> int:
    """
    calculates the safety factor of the robots
    divide the positions into four equally sized
    quadrants, ignoring the center row and column
    for each quadrant, count the number of robots
    return the product of the number of robots in each quadrant
    """
    max_x, max_y = max_position
    center_x, center_y = max_x // 2, max_y // 2
    quadrants = [[] for _ in range(4)]
    for robot in robots:
        quadrants[0].append(robot[0] < center_x and robot[1] < center_y)
        quadrants[1].append(robot[0] < center_x and robot[1] > center_y)
        quadrants[2].append(robot[0] > center_x and robot[1] < center_y)
        quadrants[3].append(robot[0] > center_x and robot[1] > center_y)
    return sum(quadrants[0]) * sum(quadrants[1]) * sum(quadrants[2]) * sum(quadrants[3])


def move_robot(
    robot: tuple[int, int],
    velocity: tuple[int, int],
    max_position: tuple[int, int],
    turns: int,
) -> tuple[int, int]:
    """moves the robot by the velocity for the number of turns
    if the robot moves past the max_position, it wraps around to the other side"""
    new_position = (robot[0] + velocity[0] * turns, robot[1] + velocity[1] * turns)
    new_position = new_position[0] % max_position[0], new_position[1] % max_position[1]
    return new_position


def main():
    """given an input of a list of robot locations and velocities
    find the final locations of the robots after x turns
    given those final positions, calculate the safety factor
    """
    turns = 100
    max_position = (101, 103)
    robots = []

    filename = "./python/2024/input/14.txt"
    with open(filename, "r", encoding="utf-8") as f:
        for line in f.readlines():
            p, v = line.strip().split(" ")
            p = tuple(int(x) for x in p.split("p=")[1].split(","))
            v = tuple(int(x) for x in v.split("v=")[1].split(","))
            robots.append((p, v))

    final_positions = []
    for robot in robots:
        final_positions.append(move_robot(robot[0], robot[1], max_position, turns))

    print_solution(get_safety_factor(final_positions, max_position))


if __name__ == "__main__":
    main()
