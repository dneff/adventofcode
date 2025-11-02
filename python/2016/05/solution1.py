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
    Advent of Code 2016 - Day 5: How About a Nice Game of Chess?

    Find an 8-character password by hashing a door ID with incrementing indices.
    For each hash that starts with five zeros (00000), the sixth character becomes
    the next character in the password.
    """
    # Read the door ID from input file
    door_id = AoCInput.read_lines(INPUT_FILE)[0].strip()

    index = 0
    password_chars = []

    # Continue until we've found all 8 password characters
    while len(password_chars) < 8:
        # Create MD5 hash of door_id + index
        h = hashlib.md5()
        h.update(str.encode(door_id + str(index)))
        hex_hash = str(h.hexdigest())

        # Check if hash starts with five zeros
        if hex_hash[:5] == '00000':
            # The sixth character (index 5) is the next password character
            password_chars.append(hex_hash[5])
            print(".",)  # Progress indicator

        index += 1

    # Join all password characters to form the final 8-character password
    password = ''.join(password_chars)
    AoCUtils.print_solution(1, password)

if __name__ == "__main__":
    main()