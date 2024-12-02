def print_solution(x):
    print(f"The solution is: {x}")


def main():
    """finds solution"""
    left, right = [], []
    filename = "./python/2024/input/01.txt"
    with open(filename, "r", encoding="utf-8") as f:
        for line in f.readlines():
            l, r = [int(x) for x in line.split()]
            left.append(l), right.append(r)

    left.sort()
    right.sort()

    differences = [abs(x - y) for x, y in zip(left, right)]
    print_solution(sum(differences))


if __name__ == "__main__":
    main()
