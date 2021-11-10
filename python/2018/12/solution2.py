import copy
from collections import defaultdict

def printSolution(x):
    print(f"The solution is {x}")

def processGeneration(rules, pots):    
    new_pots = ['.'] * len(pots)

    for idx in range(len(pots)):
        rule_key = ''.join(pots[idx-2:idx+3])
        if rule_key in rules.keys():
            new_pots[idx] = rules[rule_key]
    
    return ''.join(new_pots)

def scorePots(pots, offset):
    score = 0
    for s in range(len(pots)):
        if pots[s] == '#':
            score += s - offset
    return score

def main():
    test = 'test.txt'
    puzzle = 'input.txt'
    offset = 2000
    active = puzzle
    total_gens = 50000000000

    rules = {}
    file = open(active, 'r')
    pots = file.readline().strip().split(' ')[-1]
    pad = '.' * offset
    pots = pad + pots + pad
    file.readline()
    for line in file.readlines():
        k,v = line.strip().split(' => ')
        rules[k] = v

    score_run = []
    gens_until_stable = 200
    for generation in range(gens_until_stable):
        pots = processGeneration(rules, pots)
        score_run.append(scorePots(pots, offset))

    score_diff = score_run[-1] - score_run[-2]
    gens_left = total_gens - gens_until_stable

    printSolution((gens_left * score_diff) + score_run[-1])
    
if __name__ == "__main__":
    main()