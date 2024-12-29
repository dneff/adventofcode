from functools import lru_cache

def print_solution(x):
    print(f"The solution is: {x}")

@lru_cache(maxsize=None)
def search_for_target(machine, position=(0,0), a_count=0, b_count=0):
    """recursive search for target
    if position is target, return button presses
    else, try each button press and recurse
    maximum button presses is 100"""
    A, B, target = machine
    solutions = set()
    if a_count > 100 or b_count > 100:
        return solutions
    if position[0] > target[0] or position[1] > target[1]:
        return solutions
    if position == target:
        solutions.add((a_count, b_count))
        return solutions
    else:
        a_pos = (position[0] + A[0], position[1] + A[1])
        solutions.update(search_for_target(machine, a_pos, a_count + 1, b_count))
        b_pos = (position[0] + B[0], position[1] + B[1])
        solutions.update(search_for_target(machine, b_pos, a_count, b_count + 1))
    return solutions

def find_cost(solution):
    """the cost of a solution is 3 * A presses + 1 * B presses"""
    return 3 * solution[0] + 1 * solution[1]


def main():
    """
    given two possible offsets for moving and a target
    point, find how many steps it takes to get to the target point
    """
    filename = "./python/2024/input/13.txt"
    with open(filename, "r", encoding="utf-8") as f:
        machines = []
        machine = {}
        for line in f.readlines():
            l = line.strip()
            if  len(l) == 0:
                machines.append((machine["A"], machine["B"], machine["prize"]))
                machine = {}
                continue
            k,v = l.split(": ")
            if k == "Button A":
                machine["A"] = tuple([int(x.split("+")[1]) for x in v.split(",")])
            elif k == "Button B":
                machine["B"] = tuple([int(x.split("+")[1]) for x in v.split(",")])  
            elif k == "Prize":
                machine["prize"] = tuple([int(x.split("=")[1]) for x in v.split(",")])
        machines.append((machine["A"], machine["B"], machine["prize"]))
    
    """find the cost of each machine"""
    machine_costs = []
    for machine in machines:
        possible_solutions = search_for_target(machine)
        if len(possible_solutions) > 0:
            for solution in possible_solutions:
                machine_costs.append(find_cost(solution))

    print_solution(sum(machine_costs))


if __name__ == "__main__":
    main()
