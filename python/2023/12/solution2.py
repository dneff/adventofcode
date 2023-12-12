"""solves 2023 day 12 part 2"""

def print_solution(x):
    """prints solution"""
    print(f"The solution is: {x}")

def validate_record(springs, counts):
    """check if spring positions match counts"""
    positions = [len(x) for x in springs.split('.') if len(x) > 0]
    return positions == counts

def next_hamming(binary):
    """
    return next binary number with same hamming weight
    algo source: https://math.stackexchange.com/a/2255452
    """
    c = binary & -binary
    r = binary + c
    next_binary = (((r^binary) >> 2) // c) | r
    return next_binary

def spring_combos(springs, record):
    """
    generator that returns all spring combinations
    use a bitmask, find max, min value of bit mask
    from min val, find next hamming weight number
    do that up to max val
    """
    hamming = sum(record) - springs.count('#')
    mask_size = springs.count('?')
    max_binary = int('1' * hamming + '0' * (mask_size - hamming),2)
    current = int('0' * (mask_size - hamming) + '1' * hamming,2)
    format_cfg = '0' + str(mask_size) + 'b'
    while current <= max_binary:
        mask = format(current, format_cfg)
        mask = mask.replace('1','#').replace('0','.')
        mask = list(mask)
        valid_combo = []
        for s in springs[:]:
            if s == '?':
                valid_combo.append(mask.pop(0))
            else:
                valid_combo.append(s)
        yield ''.join(valid_combo)
        if current == max_binary:
            break
        current = next_hamming(current)



def main():
    """main"""
    expansion = 5
    lines = []
    filename = "./python/2023/input/12-test.txt"
    with open(filename, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file.readlines()]

    valid_combos = []
    total_records = len(lines)
    current_records = 0
    for record in lines:
        springs, counts = record.split()
        print(springs, counts)
        counts = [int(x) for x in counts.split(',')]
        springs = ''.join(springs * expansion)
        counts = counts * expansion
        print(springs, counts)

        #print(springs, counts)
        possible = spring_combos(springs, counts)
        valid_count = 0
        for p in possible:
            valid = validate_record(p,counts)
            #print(p, valid)
            if valid:
                valid_count += 1
        valid_combos.append(valid_count)
        current_records += 1
        print(f"{current_records}/{total_records} complete")


    #print(valid_combos)
    print_solution(sum(valid_combos))


if __name__ == "__main__":
    main()
