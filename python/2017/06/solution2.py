import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/6/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils
from collections import defaultdict


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
    allocation_history = defaultdict(list)
    memory_banks = [int(x) for x in line.strip().split()]

    reallocate_count = 0
    memory_bank_history.add(tuple(memory_banks))
    allocation_history[tuple(memory_banks)].append(reallocate_count)

    new_mem = reallocate(memory_banks)
    reallocate_count += 1

    while tuple(new_mem) not in memory_bank_history:
        memory_bank_history.add(tuple(new_mem))
        allocation_history[tuple(new_mem)].append(reallocate_count)

        new_mem = reallocate(new_mem)
        reallocate_count += 1

    # solution is current count - last count for current mem
    AoCUtils.print_solution(2, reallocate_count - allocation_history[tuple(new_mem)][0])


if __name__ == "__main__":
    main()
