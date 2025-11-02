def AoCUtils.print_solution(2, x):
    print(f"The solution is: {x}")
def getPosition(modulus, start_position, time):
    return (start_position + time) % modulus
def main():
    device = {}
import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2016/15/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils

    for idx, line in enumerate(file):
        l = line.strip().split()
        device[idx] = {'mod': int(l[3]), 'position': int(l[-1][:-1])}

    device[len(device.keys())] = {'mod': 11, 'position': 0}
    
    time = 0
    searching = True
    while searching:
        alignment = [getPosition(device[k]['mod'],device[k]['position'], time+1+k) for k in range(len(device.keys()))]
        if sum(alignment) == 0:
            searching = False
        else:
            time += 1

    AoCUtils.print_solution(2, time)

if __name__ == "__main__":
    main()