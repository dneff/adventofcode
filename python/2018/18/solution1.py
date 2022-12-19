from collections import defaultdict



def print_solution(x):
    """formats input for printing"""
    print(f"The solution is: {x}")


def get_adjacent(area, position):
    x, y = position
    adjacents = [(x - 1, y + 1), (x, y + 1), (x + 1, y + 1),
                 (x - 1, y), (x + 1, y),
                 (x - 1, y - 1), (x, y - 1), (x + 1, y - 1)]
    result = defaultdict(int)
    for p in adjacents:
        if p in area.keys():
            result[area[p]] += 1
    return result

def resource_value(area):
    trees = list(area.values()).count('|')
    lumber = list(area.values()).count('#')
    return trees * lumber

def update_acre(area, position):
    acre = area[position]
    surrounding = get_adjacent(area, position)
    if acre == '.':
        if surrounding['|'] >= 3:
            acre = '|'
    elif acre == '|':
        if surrounding['#'] >= 3:
            acre = '#'
    elif acre == '#':
        if surrounding['#'] > 0 and surrounding['|'] > 0:
            pass
        else:
            acre = '.'

    return acre


def main():
    file = open('input.txt', 'r', encoding='utf-8')
    area = {}
    for y, line in enumerate(file.readlines()):
        for x, char in enumerate(line.strip()):
            area[(x, y)] = char


    time_limit = 10
    for minute in range(time_limit):
        new_area = {}
        for position in area:
            new_area[position] = update_acre(area, position)
        area = new_area

    print_solution(resource_value(area))


if __name__ == "__main__":
    main()
