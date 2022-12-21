
def printSolution(x):
    print(f"The solution is: {x}")

def main():
    file = open('../input/07.txt', 'r', encoding='utf-8')
    objpath = []
    files = {}
    dirs = set()
    for line in file.readlines():
        if '$ cd ' in line:
            nextDir = line.strip().split()[-1]
            if nextDir == '..':
                objpath.pop()
            elif nextDir == '/':
                pass
            else:
                objpath.append(nextDir)
        elif 'dir ' in line:
            dirpath = objpath[:] + [line.strip().split()[-1]]
            dirs.add('/'+'/'.join(dirpath))
        elif line[0].isdigit():
            size, filename = line.split()
            filepath = objpath[:] + [filename]
            files['/'+'/'.join(filepath)] = int(size)

    dirsizes = {}
    for d in dirs:
        size = 0
        for filepath, weight in files.items():
            if d in filepath:
                size += weight
        dirsizes[d] = size
    
    bigdirs = [v for v in dirsizes.values() if v <= 100000]

    printSolution(sum(bigdirs))

if __name__ == "__main__":
    main()