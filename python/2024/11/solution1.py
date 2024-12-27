def print_solution(x):
    print(f"The solution is: {x}")

def blink(stones):
    """for each stone, apply the first validrule
        - if the stone is 0, replace with 1
        - if the stone has an even number of digits, split into two stones
        - if no other rules apply, multiply the stone by 2024
    """
    skip = False
    for i, stone in enumerate(stones):
        if skip:
            skip = False
            continue
        if stone == 0:
            stones[i] = 1
        elif len(str(stone)) % 2 == 0:
            left, right = str(stone)[:len(str(stone))//2], str(stone)[len(str(stone))//2:]
            stones[i] = int(left)
            stones.insert(i + 1, int(right))
            skip = True
        else:
            stones[i] = stone * 2024
    return stones

def main():
    """given a sequence of numbers, apply a function to the sequence
        n number of times, and return the result"""

    filename = "./python/2024/input/11.txt"
    with open(filename, "r", encoding="utf-8") as f:
        stones = [int(x) for x in f.readline().split()]
        blinks = 25
        for current_blink in range(blinks):
            stones = blink(stones)
        print_solution(len(stones))

if __name__ == "__main__":
    main()
