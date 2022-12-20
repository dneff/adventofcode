from collections import defaultdict

def printSolution(x):
    print(f"The solution is: {x}")

def moveCrates(cargo, count, src, dest):
    grab = cargo[src][-count:]
    cargo[src] = cargo[src][:-count]
    cargo[dest].extend(grab)



def main():
    file = open('../input/05.txt', 'r', encoding='utf-8')
    cargo = defaultdict(list)
    for line in file.readlines():
        if line.strip()[0] == '1':
            break
        for i,c in enumerate(line.rstrip()):
            if c not in [' ','[',']']:
                cargo[1+(i//4)].insert(0,c)
    
    file.seek(0)
    blank = False
    for line in file.readlines():
        if not blank:
            blank = line.strip() == ''
            continue
        instruction = line.rstrip().split()
        moveCrates(cargo, int(instruction[1]), int(instruction[3]), int(instruction[5]))
    topCrates = [cargo[x][-1] for x in range(1, len(cargo)+ 1)]
    printSolution(''.join(topCrates))
        

if __name__ == "__main__":
    main()