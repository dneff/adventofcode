
from collections import defaultdict
from datetime import datetime

def printSolution(x):
    print(f"The solution is {x}")

def main():
    log = []
    file = open('input.txt', 'r')
    for line in file:
        log.append(line.strip())
    log.sort()

    date_format= '%Y-%m-%d %H:%M'

    guards = defaultdict(lambda: defaultdict(int))
    current_guard = ''

    idx = 0
    while idx < len(log):
        entry = log[idx].split()
        if entry[2] == 'Guard':
            current_guard = int(entry[3][1:])
        elif entry[2] == 'falls':
            start = log[idx].split(']')[0][1:]
            start = datetime.strptime(start, date_format)
            idx += 1
            end = log[idx].split(']')[0][1:]
            end = datetime.strptime(end, date_format)
            for m in range(start.minute, end.minute):
                guards[current_guard][m] += 1

        idx += 1

    guard_slept = [(x,sum(y.values())) for x,y in guards.items()]
    guard_slept.sort(key = lambda x: x[1], reverse=True)

    sleepiest = guard_slept[0][0]
    sleepiest_minute = max(guards[sleepiest], key=guards[sleepiest].get)

    printSolution(sleepiest * sleepiest_minute)
    
    


if __name__ == "__main__":
    main()