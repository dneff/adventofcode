"""
Advent of Code 2016 - Day 21: Scrambled Letters and Hash (Part 2)

This solution unscrambles a password by finding the original password that,
when scrambled using the given operations, produces the target scrambled password.

Part 2 asks: Given the scrambled password "fbgdceah", what was the unscrambled
password before applying all the scrambling operations?

The solution uses a brute-force approach by trying all possible permutations
of the scrambled password and checking which one produces the target when scrambled.
"""
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, "../../../../aoc-data/2016/21/input")
sys.path.append(os.path.join(SCRIPT_DIR, "../../"))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

from itertools import permutations  # noqa: E402


class Scrambler:
    """
    Password scrambler that applies various operations to transform a password string.

    Supports six types of scrambling operations:
    - swap_position: Swap characters at two positions
    - swap_letter: Swap all occurrences of two letters
    - rotate_left/rotate_right: Rotate the entire string
    - rotate_position: Rotate based on a letter's position
    - reverse: Reverse a substring
    - move: Move a character from one position to another

    In Part 2, this class preloads all operations and can replay them
    to test different starting passwords.
    """

    def __init__(self, password):
        """Initialize the scrambler with a starting password."""
        self.password = password
        self.data = []  # Stores the sequence of operations to apply

    def load(self, filepath):
        """Load and parse all scrambling operations from the input file."""
        for line in AoCInput.read_lines(filepath):
            inst = line.strip().split(" ")
            if inst[0] in ["move", "reverse"]:
                method = inst[0]
            else:
                method = "_".join([inst[0], inst[1]])
            method = method.replace("based", "position")
            args = []
            for a in [inst[2], inst[-1]]:
                if len(a) == 1:
                    if a.isdigit():
                        args.append(int(a))
                    else:
                        args.append(a)
            self.data.append((method, args))

    def compile(self):
        """Execute all loaded scrambling operations in sequence."""
        for i in self.data:
            method, args = i
            step = getattr(self, method)
            step(*args)

    def swap_position(self, a, b):
        """Swap characters at positions a and b (0-indexed)."""
        x = min(a, b)
        y = max(a, b)
        x_letter = self.password[x]
        y_letter = self.password[y]
        self.password = (
            self.password[:x]
            + y_letter
            + self.password[x + 1:y]
            + x_letter
            + self.password[y + 1:]
        )

    def swap_letter(self, x, y):
        """Swap all occurrences of letter x with letter y."""
        self.password = self.password.replace(x, "_1_")
        self.password = self.password.replace(y, "_2_")
        self.password = self.password.replace("_1_", y)
        self.password = self.password.replace("_2_", x)

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
        idx += 1
        self.rotate_right(idx)

    def reverse(self, a, b):
        """Reverse the substring from position a through position b (inclusive)."""
        x, y = min(a, b), max(a, b)
        self.password = (
            self.password[:x]
            + "".join(list(reversed(self.password[x:y + 1])))
            + self.password[y + 1:]
        )

    def move(self, x, y):
        """Remove the character at position x and insert it at position y."""
        letter_x = self.password[x]
        self.password = self.password[:x] + self.password[x + 1:]
        self.password = self.password[:y] + letter_x + self.password[y:]


def main():
    """
    Unscramble the password by finding which starting password produces the target.

    Given the scrambled password "fbgdceah", this function tries all possible
    permutations to find which original password, when scrambled using the
    operations from the input file, produces the target scrambled password.

    This is a brute-force approach that works for passwords of reasonable length.
    """
    # Test configuration (unused in actual puzzle)
    test = {"pwd": "abcde", "file": "test.txt"}  # noqa: F841

    # Puzzle configuration
    puzzle = {"pwd": "abcdefgh", "file": INPUT_FILE}

    active = puzzle

    # Initialize scrambler and load all operations
    scrambler = Scrambler("")
    scrambler.load(active["file"])

    # The target scrambled password we need to reverse
    target_scrambled_password = "fbgdceah"

    # Try all permutations to find the original unscrambled password
    for candidate_password in permutations(target_scrambled_password):
        candidate_password = "".join(candidate_password)

        # Apply scrambling operations to this candidate
        scrambler.password = candidate_password
        scrambler.compile()

        # Check if this candidate produces the target when scrambled
        if scrambler.password == target_scrambled_password:
            AoCUtils.print_solution(2, candidate_password)
            break


if __name__ == "__main__":
    main()
