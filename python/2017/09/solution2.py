
def print_solution(x):
    """ prints input with sol'n formatting """
    print(f"The solution is: {x}")


def filter_garbage(stream):
    """return all garbage from string"""
    clean = []
    unclean = []
    offset = 0
    garbage = False
    while offset < len(stream):
        if stream[offset] == '!':
            offset += 1
        elif stream[offset] == '<':
            if garbage is False:
                garbage = True
            else:
                unclean.append(stream[offset])
        elif stream[offset] == '>':
            garbage = False
        elif garbage is False:
            clean.append(stream[offset])
        elif garbage is True:
            unclean.append(stream[offset])
        offset += 1
    return ''.join(unclean)


def main():
    file = open('input.txt', 'r', encoding='utf-8')
    stream = file.readline().strip()
    print_solution(len(filter_garbage(stream)))


if __name__ == "__main__":
    main()
