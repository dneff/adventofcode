
from collections import defaultdict
from string import ascii_uppercase

def printSolution(x):
    print(f"The solution is {x}")

def main():
    puzzle = 'input.txt'
    test = 'test.txt'
    active = puzzle

    steps = defaultdict(list)
    requirements = defaultdict(list)

    file = open(active, 'r')
    for line in file:
        _,start,_,_,_,_,_,end,_,_= line.strip().split()
        steps[start].append(end)
        requirements[end].append(start)

    # find first step    
    last = [x for sublist in steps.values() for x in sublist]
    first = set(steps.keys()) - set(last)

    completed = []
    active = defaultdict(int)


    workers = 5
    base_time = 60
    timer = 0

    for c in first:
        active[c] = ascii_uppercase.find(c) + base_time + 1

    while active or len(completed) < 26:
        if len(active.keys()) < workers:
            possible = []
            for done in completed:
                for new_step in steps[done]:
                    if new_step not in active.keys() and new_step not in completed:
                        if new_step not in requirements.keys() or set(requirements[new_step]) <= set(completed):
                            possible.append(new_step)
            possible.sort()
            while possible and len(active.keys()) < workers:
                new_step = possible.pop(0)
                active[new_step] = ascii_uppercase.find(new_step) + base_time + 1

        for s in list(active.keys()):
            active[s] -= 1
            if active[s] <= 0:
                active.pop(s)
                completed.append(s)
        timer += 1
    
    printSolution(timer)


if __name__ == "__main__":
    main()