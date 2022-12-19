
def main():
    entries = {}
    target_sum = 2020
    solution = 0

    file = open('input.txt', 'r')

    for line in file:
        entries[int(line.strip())] = ''

    for x in entries.keys():
        sub_target = target_sum - x
        for y in entries.keys():
            if y == x:
                continue
            z = sub_target - y
            if z in entries.keys():
                solution = x*y*z
                break

    print(f"The solution is: {solution}")

if __name__ == "__main__":
    main()