import copy

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
    offset = 50
    active = test

    rules = {}
    file = open(active, 'r')
    pots = file.readline().strip().split(' ')[-1]
    pad = '.' * offset
    pots = pad + pots + pad
    file.readline()
    for line in file.readlines():
        k,v = line.strip().split(' => ')
        rules[k] = v

    for generation in range(1,21):
        pots = processGeneration(rules, pots)

    printSolution(scorePots(pots, offset))
    
if __name__ == "__main__":
    main()