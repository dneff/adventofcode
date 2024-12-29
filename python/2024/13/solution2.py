def print_solution(x: int) -> None:
    """Print the final solution in a formatted string.
    
    Args:
        x (int): The solution value to print
    """
    print(f"The solution is: {x}")


def search_for_target(machine: tuple[tuple[int, int], tuple[int, int], tuple[int, int]]) -> tuple[int, int] | None:
    """Solve a system of linear equations using Cramer's rule to find button press combinations.
    
    Cramer's rule is used to solve the system:
    a*A_x + b*B_x = target_x
    a*A_y + b*B_y = target_y
    
    where (a,b) are the number of button presses we're solving for.
    
    Args:
        machine (tuple): Contains three tuples (A, B, target) where:
            - A: (x, y) offset for button A
            - B: (x, y) offset for button B
            - target: (x, y) target coordinates
    
    Returns:
        tuple[int, int] | None: Returns (a, b) number of button presses if solution exists,
                                None if no integer solution exists or if system is singular
    """
    A, B, target = machine
    determinant = A[0] * B[1] - A[1] * B[0]
    if determinant == 0:
        return None
    a_x = (target[0] * B[1] - target[1] * B[0]) / determinant
    a_y = (target[1] * A[0] - target[0] * A[1]) / determinant
    if (a_x).is_integer() and (a_y).is_integer():
        return (int(a_x), int(a_y))
    return None


def find_cost(solution: tuple[int, int]) -> int:
    """Calculate the total cost based on button press combinations.
    
    Args:
        solution (tuple[int, int]): Number of presses for each button (a, b)
    
    Returns:
        int: Total cost where button A costs 3 and button B costs 1
    """
    return 3 * solution[0] + solution[1]


def main() -> None:
    """Process arcade machine data and find optimal button press combinations.
    
    Reads machine configurations from a file where each machine has:
    - Button A: x,y offset when pressed
    - Button B: x,y offset when pressed
    - Prize: target x,y coordinates
    
    The actual target is offset by 10^13 in both x and y directions.
    
    Calculates the minimum cost to reach each prize and sums the total.
    """
    filename = "./python/2024/input/13.txt"
    with open(filename, "r", encoding="utf-8") as f:
        machines = []
        machine = {}
        for line in f.readlines():
            l = line.strip()
            if len(l) == 0:
                machines.append((machine["A"], machine["B"], machine["prize"]))
                machine = {}
                continue
            k, v = l.split(": ")
            if k == "Button A":
                machine["A"] = tuple([int(x.split("+")[1]) for x in v.split(",")])
            elif k == "Button B":
                machine["B"] = tuple([int(x.split("+")[1]) for x in v.split(",")])
            elif k == "Prize":
                machine["prize"] = tuple([int(x.split("=")[1]) for x in v.split(",")])
                machine["prize"] = (
                    machine["prize"][0] + 10000000000000,
                    machine["prize"][1] + 10000000000000,
                )
        machines.append((machine["A"], machine["B"], machine["prize"]))

    """find the cost of each machine"""
    machine_costs = []
    for machine in machines:
        solution = search_for_target(machine)
        if solution is not None:
            machine_costs.append(find_cost(solution))

    print_solution(sum(machine_costs))


if __name__ == "__main__":
    main()
