from collections import deque


def print_solution(x):
    """ formats solution and prints """
    print(f"The solution is: {x}")


def main():
    """main solution for problem"""
    file = open('input.txt', 'r', encoding='utf-8')
    instructions = [int(x) for x in file.readline().strip().split(',')]
    offset = 0
    skip_size = 0
    ring = deque()
    ring.extend(range(256))

    for i in instructions:
        flip, keep = list(ring)[:i], list(ring)[i:]
        flip.reverse()
        ring = deque(flip + keep)

        ring.rotate(-((i + skip_size) % len(ring)))

        offset += i + skip_size
        skip_size += 1

    ring.rotate(offset)
    print_solution(ring[0] * ring[1])


if __name__ == "__main__":
    main()
