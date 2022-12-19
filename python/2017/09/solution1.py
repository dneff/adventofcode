
def print_solution(x):
    """ prints input with sol'n formatting """
    print(f"The solution is: {x}")


def clean_garbage(stream):
    """remove all garbage from string"""
    clean = []
    offset = 0
    garbage = False
    while offset < len(stream):
        if stream[offset] == '<':
            garbage = True
        elif stream[offset] == '!':
            offset += 1
        elif stream[offset] == '>':
            garbage = False
        elif garbage is False:
            clean.append(stream[offset])
        offset += 1
    return ''.join(clean)


def score_stream(stream):
    """ score brackets in stream """
    score = 0
    depth = 0
    offset = 0
    while offset < len(stream):
        if stream[offset] == '{':
            depth += 1
        elif stream[offset] == '}':
            score += depth
            depth -= 1
        offset += 1

    return score


def main():
    file = open('input.txt', 'r', encoding='utf-8')
    stream = file.readline().strip()
    stream = clean_garbage(stream)
    print_solution(score_stream(stream))


if __name__ == "__main__":
    main()
