
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

    disk_total = 70000000
    disk_free_target = 30000000
    disk_used = sum(files.values())
    disk_free = disk_total - disk_used
    delete_target = disk_free_target - disk_free
    
    for d in dirs:
        size = 0
        for filepath, weight in files.items():
            if d in filepath:
                size += weight
        dirsizes[d] = size
    
    target_dir = disk_total
    for v in dirsizes.values():
        if v >= delete_target:
            target_dir = min(target_dir, v)

    printSolution(target_dir)

if __name__ == "__main__":
    main()