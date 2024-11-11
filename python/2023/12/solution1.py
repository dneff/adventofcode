import functools

@functools.cache
def calc (record, groups):

    if not groups:
        if "#" not in record:
            return 1
        else:
            return 0

    if not record:
        return 0

    next_char = record[0]
    next_group = groups[0]

    def pound():
        this_group = record[:next_group]
        this_group = this_group.replace("?", "#")

        if this_group != next_group * "#":
            return 0

        if len(record) == next_group:
            if len(groups) == 1:
                return 1
            else:
                return 0
        if record[next_group] in "?.":
            return calc(record[next_group+1:], groups[1:])
        
        return 0

    
    def dot():
        return calc(record[1:], groups)
    
    if next_char == '#':
        out = pound()
    elif next_char == '.':
        out = dot()
    elif next_char == '?':
        out = dot() + pound()
    else:
        raise RuntimeError
    
    #print(f"{record} {groups} -> {out}")
    #print(10*"-")

    return out


def main():
    filename = "./python/2023/input/12.txt"
    with open(filename, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file.readlines()]

    output = 0

    for entry in lines:
            record, group = entry.split()
            groups = [int(i) for i in group.split(',')]

            output += calc(record, tuple(groups))

    print(f"The result is: {output}")

if __name__ == "__main__":
    main()