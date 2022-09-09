
def print_solution(x):
    """format input for printing"""
    print(f"The solution is: {x}")


def main():
    ring = 1
    cycle_size = 50000000
    step_size = 328
    idx = 0
    result = 0
    for i in range(1, cycle_size):
        idx = (idx + step_size) % ring
        ring += 1
        idx += 1
        if idx == 1:
            result = i
    print_solution(result)


if __name__ == "__main__":
    main()
