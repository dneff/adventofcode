"""solves 2023 day 19 problem 2"""
from collections import defaultdict
from copy import deepcopy


def print_solution(x):
    """ "prints solution"""
    print(f"The solution is: {x}")


def parse_input(lines):
    """parses input and returns instruction dict and parts list"""
    instructions = {}
    parts = []
    inst_complete = False
    for l in lines:
        if len(l.strip()) == 0:
            inst_complete = True
            continue
        if inst_complete:
            p = l.strip().strip("{}").split(",")
            part = {}
            for attr in p:
                k, v = attr.split("=")
                part[k] = int(v)
            parts.append(part.copy())
        else:
            k, v = l.strip().split("{")
            v = v[:-1]
            instructions[k] = v.split(",")

    queues = defaultdict(list)
    for part in parts:
        queues["in"].append(part)

    return queues, instructions


def route_part(part, queue_instructions):
    """given a part and queue instructions, figure out next queue"""
    for instruction in queue_instructions:
        if ":" in instruction:
            attr = instruction[0]
            condition = instruction[1]
            comp, route = instruction[2:].split(":")
            comp = int(comp)
            if condition == "<" and part[attr] < comp:
                return route
            if condition == ">" and part[attr] > comp:
                return route
        else:
            return instruction


def score_part(part):
    """given a part, return score"""
    x = part["x"][1] - part["x"][0] + 1
    m = part["m"][1] - part["m"][0] + 1
    a = part["a"][1] - part["a"][0] + 1
    s = part["s"][1] - part["s"][0] + 1
    for v in [x, m, a, s]:
        if v <= 0:
            return 0
    return x * m * a * s


def main():
    """loads input and solves problem"""
    lines = []
    filename = "./python/2023/input/19-test.txt"
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]

    queues, instructions = parse_input(lines)

    # find instruction paths to accept/reject outcomes
    # for each queue, route each part to the next queue
    # if queue is "accept" or "reject", add to accept/reject list
    accept_path = []
    reject_path = []

    paths = defaultdict(lambda: defaultdict(str))
    for i, rules in instructions.items():
        for rule in rules:
            if ":" in rule:
                attr = rule[0]
                condition = rule[1]
                comp, route = rule[2:].split(":")
                comp = int(comp)
                paths[i][route] = (attr, condition, comp)
            else:
                paths[i][rule] = ()

    all_paths = []
    queue = [["in"]]
    while queue:
        path = queue.pop()
        for next_path, rule in paths[path[-1]].items():
            if next_path in path:
                continue  # avoid loops
            if next_path in ["A"]:
                all_paths.append(path + [rule] + [next_path])
            elif next_path in ["R"]:
                continue
            else:
                queue.append(path + [rule] + [next_path])

    possible_parts = 0

    primitive = {"x": [1, 4000], "m": [1, 4000], "a": [1, 4000], "s": [1, 4000]}

    all_parts = []
    for path in all_paths:
        part = deepcopy(primitive)
        for rule in path:
            if len(rule) == 3:
                attr, condition, comp = rule
                if condition == "<":
                    part[attr][1] = min(part[attr][1], comp - 1)
                elif condition == ">":
                    part[attr][0] = max(part[attr][0], comp + 1)
        all_parts.append(part)

    score = 0
    for part in all_parts:
        print(score_part(part))
        score += score_part(part)

    print_solution(167409079868000)
    print_solution(score)


if __name__ == "__main__":
    main()
