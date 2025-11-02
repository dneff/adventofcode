import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2016/10/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils
from collections import defaultdict
import math

def main():
    instructions = defaultdict(list)
    bot = defaultdict(list)
    output = defaultdict(list)    
    input = []

    def processBot(bot_id):
        chips = bot[bot_id][:]
        chips.sort()
        bot[bot_id].clear()
        for idx, i in enumerate(instructions[bot_id]):
            if i[0] == 'output':
                output[i[1]].append(chips[idx])
            else:
                bot[i[1]].append(chips[idx])
                if len(bot[i[1]]) == 2:
                    processBot(i[1])

    lines = AoCInput.read_lines(INPUT_FILE)
    for line in lines:
        line = line.strip().split()
        if line[0] == "bot":
            instructions[line[1]] = [(line[-7],line[-6]), (line[-2],line[-1])]
        else:
            input.append([line[-1],int(line[1])])
    
    for i in input:
        robot, chip = i
        bot[robot].append(chip)
        if len(bot[robot]) == 2:
            processBot(robot)
    
    AoCUtils.print_solution(2, output['0'].pop() * output['1'].pop() * output['2'].pop())
    
if __name__ == "__main__":
    main()