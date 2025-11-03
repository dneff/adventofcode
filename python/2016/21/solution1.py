"""
Advent of Code 2016 - Day 21: Scrambled Letters and Hash (Part 1)

This solution implements a password scrambler that applies a series of operations
to transform an initial password string. The operations include swapping positions,
swapping letters, rotating, reversing subsequences, and moving characters.

The goal is to determine the scrambled password after applying all operations
to the initial password "abcdefgh".
"""
import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2016/21/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


class Scrambler():
    """
    Password scrambler that applies various operations to transform a password string.

    Supports six types of scrambling operations:
    - swap_position: Swap characters at two positions
    - swap_letter: Swap all occurrences of two letters
    - rotate_left/rotate_right: Rotate the entire string
    - rotate_position: Rotate based on a letter's position
    - reverse: Reverse a substring
    - move: Move a character from one position to another
    """

    def __init__(self, password):
        """Initialize the scrambler with a starting password."""
        self.password = password
        self.data = ''  # Unused in Part 1, kept for compatibility

    def swap_position(self, a, b):
        """Swap characters at positions a and b (0-indexed)."""
        x = min(a,b)
        y = max(a,b)
        x_letter = self.password[x]
        y_letter = self.password[y]
        self.password = self.password[:x] + y_letter + self.password[x+1:y] + x_letter + self.password[y+1:]


    def swap_letter(self, x, y):
        """Swap all occurrences of letter x with letter y."""
        self.password = self.password.replace(x, '_1_')
        self.password = self.password.replace(y, '_2_')
        self.password = self.password.replace('_1_', y)
        self.password = self.password.replace('_2_', x)


    def rotate_left(self, x):
        """Rotate the password left by x steps."""
        x = x % len(self.password)
        self.password = self.password[x:] + self.password[:x]


    def rotate_right(self, x):
        """Rotate the password right by x steps."""
        x = x % len(self.password)
        self.password = self.password[-x:] + self.password[:-x]


    def rotate_position(self, x):
        """
        Rotate based on position of letter x.

        The password is rotated to the right based on the index of letter x:
        - Rotate right by (1 + index) steps
        - If index >= 4, rotate one additional time
        """
        idx = self.password.find(x)
        if idx >= 4:
            idx += 1
        idx +=1
        self.rotate_right(idx)
        

    def reverse(self, a, b):
        """Reverse the substring from position a through position b (inclusive)."""
        x, y = min(a, b), max(a, b)
        self.password = self.password[:x] + ''.join(list(reversed(self.password[x:y+1]))) + self.password[y+1:]


    def move(self, x, y):
        """Remove the character at position x and insert it at position y."""
        letter_x = self.password[x]
        self.password = self.password[:x] + self.password[x+1:]
        self.password = self.password[:y] + letter_x + self.password[y:]
    

def main():
    """
    Scramble the password by applying all operations from the input file.

    Starts with the password 'abcdefgh' and applies each scrambling operation
    in sequence to produce the final scrambled password.
    """
    # Test configuration for the example in the problem
    test = {
        'pwd': 'abcde',
        'file': 'test.txt'
    }

    # Puzzle configuration with the actual starting password
    puzzle = {
        'pwd': 'abcdefgh',
        'file': 'input.txt'
    }

    active = puzzle

    # Initialize scrambler with starting password
    scrambler = Scrambler(active['pwd'])

    # Process each scrambling operation from the input file
    for line in AoCInput.read_lines(INPUT_FILE):
        instruction = line.strip().split(' ')

        # Parse operation type from instruction
        # "move position X to position Y" -> "move"
        # "reverse positions X through Y" -> "reverse"
        # "swap position X with position Y" -> "swap_position"
        # "rotate based on position of letter X" -> "rotate_position"
        if instruction[0] in ['move', 'reverse']:
            method_name = instruction[0]
        else:
            method_name = '_'.join([instruction[0], instruction[1]])
        method_name = method_name.replace('based', 'position')

        # Extract arguments (positions or letters) from instruction
        args = []
        for arg in [instruction[2], instruction[-1]]:
            if len(arg) == 1:
                if arg.isdigit():
                    args.append(int(arg))
                else:
                    args.append(arg)

        # Execute the scrambling operation
        operation = getattr(scrambler, method_name)
        operation(*args)

    AoCUtils.print_solution(1, scrambler.password)
    


if __name__ == "__main__":
    main()