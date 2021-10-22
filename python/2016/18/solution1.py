
def printSolution(x):
    print(f"The solution is {x}")

def generateTile(trio):
    # traps are ones, else zero
    convert = {
        '...': '.',
        '..^': '^',
        '.^.': '.',
        '.^^': '^',
        '^..': '^',
        '^.^': '.',
        '^^.': '^',
        '^^^': '.',
        }
    return convert[trio]

def generateRow(row):
    padded_row = '.' + row + '.'
    result = ''
    for idx in range(len(padded_row) - 2):
        result += generateTile(padded_row[idx:idx+3])

    return result

def countSafe(row):
    return row.count('.')

def main():
    test = {
        'row': ".^^.^.^^^^",
        'count': 10
    }

    puzzle1 = { 
        'row': "^..^^.^^^..^^.^...^^^^^....^.^..^^^.^.^.^^...^.^.^.^.^^.....^.^^.^.^.^.^.^.^^..^^^^^...^.....^....^.",
        'count': 40
    }

    puzzle2 = { 
        'row': "^..^^.^^^..^^.^...^^^^^....^.^..^^^.^.^.^^...^.^.^.^.^^.....^.^^.^.^.^.^.^.^^..^^^^^...^.....^....^.",
        'count': 400000
    }

    active = puzzle2

    safe_tiles = 0
    row_count = 0

    current_row = active['row']
    row_count +=1

    safe_tiles += countSafe(current_row)
    while row_count < active['count']:
        current_row = generateRow(current_row)
        safe_tiles += countSafe(current_row)
        row_count += 1

    printSolution(safe_tiles)

if __name__ == "__main__":
    main()