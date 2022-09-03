
def print_solution(x):
    """ print solution """
    print(f"The solution is: {x}")


def main():
    """ calculate solution """
    f = open('input.txt', 'r', encoding='utf-8')
    digits = [int(x) for x in f.readline().strip()]

    same_sum = 0
    half = len(digits)//2
    for i, _ in enumerate(digits):
        # if digit halfway around matches,the add to same_sum
        compare = (i + half) % len(digits)
        if digits[i] == digits[compare]:
            same_sum += digits[i]
    print_solution(same_sum)


if __name__ == "__main__":
    main()
