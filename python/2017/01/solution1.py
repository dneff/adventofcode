
def print_solution(x):
    """ prints solution """
    print(f"The solution is: {x}")


def main():
    """ calculates solution """
    f = open('input.txt', 'r', encoding='utf-8')
    digits = [int(x) for x in f.readline().strip()]

    same_sum = 0
    for i in range(len(digits) - 1):
        # if the next digit matches,the add to same_sum
        if digits[i] == digits[i + 1]:
            same_sum += digits[i]
    if digits[0] == digits[-1]:
        same_sum += digits[0]
    print_solution(same_sum)


if __name__ == "__main__":
    main()
