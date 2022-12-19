
from operator import ge


def print_solution(x):
    """Format input for solution printing"""
    print(f"The solution is: {x}")

def generator(factor, seed):
    val = seed
    while True:
        val = val * factor
        val = val % 2147483647
        yield val


def main():
    factor_a = 16807
    seed_a   = 873

    factor_b = 48271
    seed_b   = 583

    gen_a = generator(factor_a, seed_a)
    gen_b = generator(factor_b, seed_b)

    matches = 0
    for _ in range(5000000):
        x = next(gen_a)
        while x % 4 != 0:
            x = next(gen_a)

        y = next(gen_b)
        while y % 8 != 0:
            y = next(gen_b)

        if format(x,'b')[-16:] == format(y,'b')[-16:]:
            matches += 1

    print_solution(matches)


if __name__ == "__main__":
    main()