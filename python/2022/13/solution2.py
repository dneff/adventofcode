from copy import deepcopy as dc


def print_solution(x):
    """
    print value passed in
    """
    print(f"The solution is {x}")


def compare(left, right):
    """
    if integers:
        If left < right, the inputs are True.
        If left > right integer, the inputs are False.
        Otherwise, continue checking the next part of the input.

    If lists:
        compare the first value of each list, then the second value, and so on.
        If the left list runs out of items first, then True.
        If the right list runs out of items first, then False.
        If the lists are the same length and no comparison makes a decision about the order, continue checking the next part of the input.

    If exactly one value is an integer:
        convert the integer to a list and retry.

    return -1, 0, 1 (False, Equal, True)
    """
    FALSE = -1
    UNKNOWN = 0
    TRUE = 1

    # both are integers
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return TRUE
        elif left > right:
            return FALSE
        return UNKNOWN

    # both are lists
    if isinstance(left, list) and isinstance(right, list):
        while len(left) != 0:
            if len(right) == 0:
                return FALSE
            test = compare(left.pop(0), right.pop(0))
            if test != UNKNOWN:
                return test

        if len(right) != 0:
            return TRUE
        return UNKNOWN

    if isinstance(left, int):
        left = [left]
    if isinstance(right, int):
        right = [right]

    return compare(left, right)


def insert_packet(packet, sorted_list):
    if len(sorted_list) != 0:
        for idx, pkt in enumerate(sorted_list):
            if compare(dc(pkt), dc(packet)) == 0:
                return
            if compare(dc(pkt), dc(packet)) < 0:
                sorted_list.insert(idx, dc(packet))
                return
    sorted_list.append(dc(packet))
    return


def main():
    sorted = []
    divider_1 = [[2]]
    divider_2 = [[6]]
    insert_packet(dc(divider_1), sorted)
    insert_packet(dc(divider_2), sorted)
    with open("../input/13.txt", "r", encoding="utf-8") as f:
        for line in f:
            if len(line.strip()) == 0:
                continue
            packet = eval(line)
            insert_packet(dc(packet), sorted)

    idx_d1 = sorted.index(divider_1) + 1
    idx_d2 = sorted.index(divider_2) + 1

    print_solution(idx_d1 * idx_d2)


if __name__ == "__main__":
    main()
