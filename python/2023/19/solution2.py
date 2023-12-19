"""solves 2023 day 19 problem 2"""
from collections import defaultdict


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


def main():
    """loads input and solves problem"""
    lines = []
    filename = "./python/2023/input/19-test.txt"
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]

    queues, instructions = parse_input(lines)

    accepted = []
    rejected = []
    processing = True
    while processing:
        processing = False
        to_process = [k for k, v in queues.items() if len(v) > 0]
        if len(to_process) > 0:
            processing = True
        for q in to_process:
            while queues[q]:
                part = queues[q].pop()
                next_q = route_part(part, instructions[q])
                if next_q == "A":
                    accepted.append(part)
                elif next_q == "R":
                    rejected.append(part)
                else:
                    queues[next_q].append(part)

    score = 0
    for part in accepted:
        score += sum(list(part.values()))
    
    print_solution(score)


if __name__ == "__main__":
    main()
