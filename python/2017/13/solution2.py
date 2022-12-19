def print_solution(x):
    """Format input for printing solution"""
    print(f"The solution is: {x}")


def main():
    file = open('input.txt', 'r', encoding='utf-8')
    firewall = {}
    for line in file.readlines():
        layer, depth = [int(x) for x in line.split(': ')]
        firewall[layer] = depth

    delay = 0
    blocked = True
    while blocked:
        for time in range(max(firewall.keys()) + 1):
            if time in firewall:
                if (time + delay) % ((firewall[time] - 1) * 2) == 0:
                    delay += 1
                    break
            if time >= max(firewall.keys()):
                blocked = False

    print_solution(delay)


if __name__ == "__main__":
    main()
