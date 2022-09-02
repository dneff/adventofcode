def print_solution(x):
    print(f"The solution is: {x}")


def main():
    f = open('input.txt', 'r')
    digits = [int(x) for x in f.readline().strip()]

    same_sum = 0
    half = len(digits)//2
    for i in range(len(digits)):
        #if digit halfway around matches,the add to same_sum
        compare = (i + half) % len(digits)
        if digits[i] == digits[compare]:
            same_sum += digits[i]
    print_solution(same_sum)


if __name__ == "__main__":
    main()
