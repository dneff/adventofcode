

def print_solution(x):
    """format input for printing"""
    print(f"The solution is: {x}")


def main():
    ring = [0]
    cycle_size = 2018
    step_size = 328
    idx = 0
    for i in range(1, cycle_size):
        idx = (idx + step_size) % len(ring)
        ring.insert(idx + 1, i)
        idx += 1

    print(ring[idx+1])


if __name__ == "__main__":
    main()
