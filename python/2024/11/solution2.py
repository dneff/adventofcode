def print_solution(x):
    print(f"The solution is: {x}")


def blink(stones):
    """for each stone, apply the first valid rule
    - if the stone is 0, replace with 1
    - if the stone has an even number of digits, split into two stones
    - if no other rules apply, multiply the stone by 2024
    """
    new_stones = {}
    for stone in stones:
        if stone == 0:
            if 1 not in new_stones:
                new_stones[1] = 0
            new_stones[1] += stones[0]
        elif len(str(stone)) % 2 == 0:
            left, right = int(str(stone)[: len(str(stone)) // 2]), int(
                str(stone)[len(str(stone)) // 2 :]
            )
            if left not in new_stones:
                new_stones[left] = 0
            if right not in new_stones:
                new_stones[right] = 0
            new_stones[left] += stones[stone]
            new_stones[right] += stones[stone]
        else:
            if stone * 2024 not in new_stones:
                new_stones[stone * 2024] = 0
            new_stones[stone * 2024] += stones[stone]
    return new_stones


def main():
    """given a sequence of numbers, apply a function to the sequence
    n number of times, and return the result"""

    filename = "./python/2024/input/11.txt"
    with open(filename, "r", encoding="utf-8") as f:
        stone_list = [int(x) for x in f.readline().split()]

    # updated to use a dictionary to store the number of stones
    stones = {}
    for stone in stone_list:
        if stone not in stones:
            stones[stone] = 0
        stones[stone] += 1
    blinks = 75
    for _ in range(blinks):
        stones = blink(stones)

    print_solution(sum(stones.values()))


if __name__ == "__main__":
    main()
