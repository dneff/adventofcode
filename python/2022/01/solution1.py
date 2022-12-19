from collections import defaultdict

def printSolution(x):
    print(f"The solution is: {x}")

def main():
    file = open('../input/01.txt', 'r', encoding='UTF-8')
    elf_packs = defaultdict(list)
    elf = 1
    for line in file.readlines():
        item = line.strip()
        if item == '':
            elf += 1
        else:
            elf_packs[elf].append(int(item))

    calories = {sum(v):k for k,v in elf_packs.items()}
    
    printSolution(max(calories.keys()))

if __name__ == "__main__":
    main()