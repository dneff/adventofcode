def print_solution(x):
    print(f"The solution is: {x}")


def main():
    """finds solution"""

    disk_map = []
    filename = "./python/2024/input/09.txt"
    with open(filename, "r", encoding="utf-8") as f:
        for line in f.readlines():
            disk_map = [int(x) for x in line.strip()]

    data_map = disk_map[::2]
    free_map = disk_map[1::2]
    blocks = []
    for i in range(len(data_map)):
        block_id = i
        block_count = data_map[i]
        for j in range(block_count):
            blocks.append(block_id)
        try:
            space_count = free_map[i]
            for j in range(space_count):
                blocks.append(".")
        except IndexError:
            pass

    """compress blocks by removing the last value and moving it to the first '.' in list"""
    """if the last value is a '.', then just remove it"""
    """continue until no more compressions are possible"""
    while "." in blocks:
        last_value = blocks.pop()
        if last_value == ".":
            continue
        first_dot = blocks.index(".")
        blocks[first_dot] = last_value

    """checksum is found by multipying a number by the index of the number in the list"""
    checksum = 0
    for i in range(len(blocks)):
        checksum += blocks[i] * i

    print_solution(checksum)


if __name__ == "__main__":
    main()
