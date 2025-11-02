import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2016/8/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


class cardReader():
    def __init__(self):
        self.height = 6
        self.width = 50
        self.screen = []
        for _ in range(self.height):
            row = ['.'] * self.width
            self.screen.append(row)

    def rect(self, w, h):
        for row in range(h):
            for col in range(w):
                self.screen[row][col] = '#'

    def rotateColumn(self, column, count):
        col = {}
        for row in range(self.height):
            col[row] = self.screen[row][column]
        for row in range(self.height):
            new_value = col[(row - count) % self.height]
            self.screen[row][column] = new_value

    def rotateRow(self, row, count):
        count = count % self.width
        self.screen[row] = self.screen[row][-count:] + \
            self.screen[row][:-count]

    def litCount(self):
        return sum([row.count('#') for row in self.screen])


def ocr_screen(screen):
    """
    OCR for 6-row tall capital letters (4 pixels wide with 1 pixel spacing).
    Returns the recognized text string.
    """
    # Letter patterns (6 rows x 4 columns, using # for lit pixels, . for off)
    patterns = {
        'A': [
            '.##.',
            '#..#',
            '#..#',
            '####',
            '#..#',
            '#..#'
        ],
        'B': [
            '###.',
            '#..#',
            '###.',
            '#..#',
            '#..#',
            '###.'
        ],
        'C': [
            '.##.',
            '#..#',
            '#...',
            '#...',
            '#..#',
            '.##.'
        ],
        'E': [
            '####',
            '#...',
            '###.',
            '#...',
            '#...',
            '####'
        ],
        'F': [
            '####',
            '#...',
            '###.',
            '#...',
            '#...',
            '#...'
        ],
        'G': [
            '.##.',
            '#..#',
            '#...',
            '#.##',
            '#..#',
            '.###'
        ],
        'H': [
            '#..#',
            '#..#',
            '####',
            '#..#',
            '#..#',
            '#..#'
        ],
        'J': [
            '..##',
            '...#',
            '...#',
            '...#',
            '#..#',
            '.##.'
        ],
        'K': [
            '#..#',
            '#.#.',
            '##..',
            '#.#.',
            '#.#.',
            '#..#'
        ],
        'L': [
            '#...',
            '#...',
            '#...',
            '#...',
            '#...',
            '####'
        ],
        'P': [
            '###.',
            '#..#',
            '#..#',
            '###.',
            '#...',
            '#...'
        ],
        'R': [
            '###.',
            '#..#',
            '#..#',
            '###.',
            '#.#.',
            '#..#'
        ],
        'S': [
            '.###',
            '#...',
            '#...',
            '.##.',
            '...#',
            '###.'
        ],
        'U': [
            '#..#',
            '#..#',
            '#..#',
            '#..#',
            '#..#',
            '.##.'
        ],
        'Z': [
            '####',
            '...#',
            '..#.',
            '.#..',
            '#...',
            '####'
        ]
    }

    # Convert screen to string format for matching
    screen_str = []
    for row in screen:
        screen_str.append(''.join(row))

    result = ''
    x = 0
    while x < len(screen_str[0]):
        # Extract 4-column slice for this letter
        letter_slice = []
        for row in screen_str:
            if x + 3 < len(row):
                letter_slice.append(row[x:x+4])
            else:
                letter_slice.append(row[x:].ljust(4, '.'))

        # Match against patterns
        found = False
        for letter, pattern in patterns.items():
            match = True
            for i in range(6):
                if letter_slice[i] != pattern[i]:
                    match = False
                    break
            if match:
                result += letter
                found = True
                break

        if not found and any('#' in row for row in letter_slice):
            result += '?'

        x += 5  # Move to next letter (4 pixels + 1 space)

    return result


def main():

    door = cardReader()

    lines = AoCInput.read_lines(INPUT_FILE)
    for line in lines:
        line = line.strip()
        line = line.replace('x=', '')
        line = line.replace('y=', '')
        line = line.replace('by', '')
        line = line.replace('x', ' ')
        line = line.replace('rotate column', 'rotateColumn')
        line = line.replace('rotate row', 'rotateRow')
        line = line.split()

        instruction = getattr(door, line[0])
        instruction(int(line[1]), int(line[2]))

    # Display the screen
    for r in door.screen:
        row = ''.join(r)
        row = row.replace('.', ' ')
        print(row)

    # OCR the result
    result = ocr_screen(door.screen)
    print()
    AoCUtils.print_solution(2, result)


if __name__ == '__main__':
    main()
