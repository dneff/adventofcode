def print_solution(x):
    print(f"The solution is: {x}")


def compress_blocks(blocks):
    """
    blocks is a list of integers and '.'
    compress blocks by replacing the rightmost block of identical integers
    with '.' and moving it to the leftmost block of '.' large enough to fit it.
    Each block is only evaluated once, from right to left.
    """
    blocks = list(blocks)  # Create a mutable copy
    processed = set()  # Keep track of positions we've already processed

    # Single pass right to left
    i = len(blocks) - 1
    while i >= 0:
        # Skip dots and processed positions
        if blocks[i] == "." or i in processed:
            i -= 1
            continue

        # Find the start of the current block
        current_num = blocks[i]
        block_start = i
        while block_start > 0 and blocks[block_start - 1] == current_num:
            block_start -= 1

        block_size = i - block_start + 1

        # Mark all positions in this block as processed
        for pos in range(block_start, i + 1):
            processed.add(pos)

        # Look for leftmost space that can fit this block
        j = 0
        while j < block_start:
            # Count consecutive dots
            if blocks[j] == ".":
                dots_start = j
                dot_count = 0
                while j < block_start and blocks[j] == ".":
                    dot_count += 1
                    j += 1

                # If we found enough space, move the block
                if dot_count >= block_size:
                    # Fill in the new position
                    for k in range(block_size):
                        blocks[dots_start + k] = current_num
                    # Clear the old position
                    for k in range(block_start, i + 1):
                        blocks[k] = "."
                    break
            else:
                j += 1

        # Move to the start of the next block from the right
        i = block_start - 1

    return blocks


def find_checksum(blocks):
    """checksum is found by multipying a number by the index of the number in the list"""
    checksum = 0
    for i in range(len(blocks)):
        if blocks[i] == ".":
            continue
        checksum += blocks[i] * i
    return checksum


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

    blocks = compress_blocks(blocks)
    checksum = find_checksum(blocks)

    print_solution(checksum)


if __name__ == "__main__":
    main()
