
def main():
    entries = {}
    target_sum = 2020
    solution = 0

    file = open('input.txt', 'r')

    for line in file:
        entries[int(line.strip())] = ''

    for x in entries.keys():
        y = target_sum - x
        if y in entries.keys():
            solution = x*y
            break
    print(f"The solution is: {solution}")


if __name__ == "__main__":
    main()