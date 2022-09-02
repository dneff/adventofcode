from collections import defaultdict

def printSolution(x) -> None:
    """ print input in formatted string """
    print(f"The solution is: {x}")


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
    file = open('input.txt', 'r')
    memory_bank_history = set()
    allocation_history = defaultdict(list)
    memory_banks = [int(x) for x in file.readline().strip().split()]

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
    printSolution(reallocate_count - allocation_history[tuple(new_mem)][0])


if __name__ == "__main__":
    main()
