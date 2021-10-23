
def printSolution(x):
    print(f"The solution is {x}")


def movePointer(elf_id, elves, moves):
    elf_pointer = elf_id
    while moves > 0:
        elf_pointer = elves[elf_pointer]
        moves -= 1

    return elf_pointer


def main():
    test = 5
    puzzle1 = 3004953

    active = puzzle1

    elves = {}
    for e in range(1, active):
        elves[e] = e+1
    elves[active] = 1
    current_elf = 1

    ring_size = active
    target_offset = ring_size//2 - 1
    half_elf = movePointer(current_elf, elves, target_offset)

    while ring_size > 2:

        if ring_size % 2 == 0:
            half_elf = elves[half_elf]

        elves[half_elf] = elves[elves[half_elf]]
        ring_size -= 1
        current_elf = elves[current_elf]

    printSolution(current_elf)
    
    

if __name__ == "__main__":
    main()