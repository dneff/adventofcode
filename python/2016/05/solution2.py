import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2016/5/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils
import string
import hashlib

def main():
    """
    Advent of Code 2016 - Day 5: How About a Nice Game of Chess? (Part 2)

    Find an 8-character password using a position-based method:
    - For hashes starting with five zeros (00000):
      - The sixth character represents the position (0-7) in the password
      - The seventh character is the character to put at that position
    - Only use the first result for each position
    - Ignore invalid positions (non-digits or positions >= 8)

    Example: Hash "000001f" means 'f' goes in position 1 of the password
    """
    # Read the door ID from input file
    door_id = AoCInput.read_lines(INPUT_FILE)[0].strip()

    index = 0
    # Initialize password with 8 empty positions (marked with '_')
    password_chars = ['_'] * 8

    # Continue until all 8 positions are filled
    while '_' in password_chars:
        # Create MD5 hash of door_id + index
        h = hashlib.md5()
        h.update(str.encode(door_id + str(index)))
        hex_hash = str(h.hexdigest())

        # Check if hash starts with five zeros
        if hex_hash[:5] == '00000':
            try:
                # The sixth character (index 5) indicates the position in the password
                position = int(hex_hash[5])

                # Only use positions 0-7 and only if not already filled
                if position < 8 and password_chars[position] == '_':
                    # The seventh character (index 6) is the password character for that position
                    password_chars[position] = hex_hash[6]
                print(".",)  # Progress indicator
            except ValueError:
                # Ignore if the sixth character is not a valid digit
                pass

        index += 1

    # Join all password characters to form the final 8-character password
    password = ''.join(password_chars)
    AoCUtils.print_solution(2, password)

if __name__ == "__main__":
    main()