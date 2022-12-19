def print_solution(x):
    """Format input for printing solution"""
    print(f"The solution is: {x}")


def main():
    file = open('input.txt', 'r', encoding='utf-8')
    firewall = {}
    for line in file.readlines():
        layer, depth = [int(x) for x in line.split(': ')]
        firewall[layer] = depth

    severity = 0
    for time in range(max(firewall.keys()) + 1):
        if time in firewall:
            if time % ((firewall[time] - 1) * 2) == 0:
                severity += firewall[time] * time

    print_solution(severity)


if __name__ == "__main__":
    main()
