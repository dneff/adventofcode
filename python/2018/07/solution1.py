
from collections import defaultdict

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
    known = list(first)

    while known:
        known.sort()
        if known:
            for i, k in enumerate(known):
                if k not in requirements.keys() or set(requirements[k]) <= set(completed):
                    completed.append(known.pop(i))
                    break
        for done in completed:
            for new_steps in steps[done]:
                if new_steps not in known and new_steps not in completed:
                    known.append(new_steps)
    printSolution(''.join(completed))

if __name__ == "__main__":
    main()