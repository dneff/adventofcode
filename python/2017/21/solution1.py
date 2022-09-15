from math import isqrt


def print_solution(x):
    """format input for printing"""
    print(f"The solution is: {x}")


def rotate_patterns(pattern):
    """ return all rotations for given pattern"""
    pattern = pattern.split('/')
    if len(pattern) == 2 and len(pattern[0]) == 2:
        pass
    elif len(pattern) == 3 and len(pattern[0]) == 3:
        pass
    else:
        raise ValueError('pattern must be only 2x2 or 3x3')
    rotations = ['/'.join(pattern)]
    # rotate three times and add
    rotated = pattern[:]
    for _ in range(3):
        rotated = list(zip(*rotated[::-1]))
        rotated = [''.join(list(x)) for x in rotated]
        rotations.append('/'.join(rotated))

    # flip top/bottom and add rotations
    flip = pattern[:]
    flip[0], flip[-1] = flip[-1], flip[0]
    rotations.append('/'.join(flip))
    for _ in range(3):
        flip = list(zip(*flip[::-1]))
        flip = [''.join(list(x)) for x in flip]
        rotations.append('/'.join(flip))

    # flip left/right and add rotations
    flip_side = pattern[:]
    flip_side = [line[::-1] for line in flip_side]
    rotations.append('/'.join(flip_side))
    for _ in range(3):
        flip_side = list(zip(*flip_side[::-1]))
        flip_side = [''.join(list(x)) for x in flip_side]
        rotations.append('/'.join(flip_side))
    return set(rotations)


def join_patterns(pattern_list):
    """join list of patterns into single pattern"""
    if not isinstance(pattern_list, list):
        raise TypeError('join_patterns: not a list')
    length = len(pattern_list)

    if length == 1:
        return pattern_list[0]
    elif length % 2 == 0:
        pass
    elif length % 3 == 0:
        pass
    else:
        raise ValueError('join_patterns: pattern list length must be divisible by 2 or 3')

    step = isqrt(length)
    final_pattern = []
    for i in range(0, length, step):
        scope = [x.split('/') for x in pattern_list[i:i + step]]
        for idx in range(len(scope[0])):
            full_row = ''.join([x[idx] for x in scope])
            final_pattern.append(full_row)

    return '/'.join(final_pattern)


def split_pattern(pattern):
    """if pattern is divisible by 2, divide into 2x2 patterns
       if pattern is divisible by 3, divide into 3x3 patterns
       else, throw an exception"""
    pattern = pattern.split('/')
    width, length = len(pattern), len(pattern[0])
    if width % 2 == 0 and length % 2 == 0:
        split_size = 2
    elif width % 3 == 0 and length % 3 == 0:
        split_size = 3
    else:
        raise ValueError('pattern width and length must be divisible by 2 or 3')

    separated = []
    for row in range(0, width, split_size):
        for col in range(0, length, split_size):
            small_pattern = []
            for i in range(split_size):
                small_pattern.append(pattern[row+i][col:col+split_size])
            separated.append('/'.join(small_pattern))
    return separated


def find_enhancement(enhancements, patterns):
    """find enhancement in pattern"""
    result = set(enhancements.keys()).intersection(set(patterns))
    if len(result) != 1:
        raise ValueError(f"find_enhancement: result not unique - {result}")
    return enhancements[result.pop()]


def main():
    file = open('input.txt', 'r', encoding='utf-8')
    enhancements = {}
    for line in file.readlines():
        k, v = line.strip().split(' => ')
        enhancements[k] = v

    cycle_count = 5
    pattern = '.#./..#/###'
    for _ in range(cycle_count):
        new_pattern = []
        separated = split_pattern(pattern)
        for p in separated:
            new_pattern.append(find_enhancement(enhancements, rotate_patterns(p)))
        pattern = join_patterns(new_pattern)

    print_solution(pattern.count('#'))


if __name__ == "__main__":
    main()
