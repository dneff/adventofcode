import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/6/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


def reallocate(memory):
    workbench = memory[:]
    pointer = workbench.index(max(workbench))
    mem = workbench[pointer]
    workbench[pointer] = 0
    while mem:
        pointer = (pointer + 1) % len(workbench)
        workbench[pointer] += 1
        mem -= 1
    return workbench


def main():
    line = AoCInput.read_lines(INPUT_FILE)[0]
    memory_bank_history = set()
    memory_banks = [int(x) for x in line.strip().split()]
    memory_bank_history.add(tuple(memory_banks))

    reallocate_count = 0
    new_mem = reallocate(memory_banks)
    reallocate_count += 1

    while tuple(new_mem) not in memory_bank_history:
        memory_bank_history.add(tuple(new_mem))
        new_mem = reallocate(new_mem)
        reallocate_count += 1

    AoCUtils.print_solution(1, reallocate_count)
    


if __name__ == "__main__":
    main()