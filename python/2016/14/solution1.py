import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2016/14/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils

from hashlib import md5
from queue import PriorityQueue
import re
from collections import defaultdict


def md5_hash_generator(salt):
    """
    Generate MD5 hashes for one-time pad key generation.

    Yields tuples of (index, hash) where hash = MD5(salt + index).

    Args:
        salt: The salt string to prepend to each index

    Yields:
        (index, hexdigest): Index number and its MD5 hash as lowercase hex string
    """
    index = 0
    while True:
        to_hash = salt + str(index)
        result = md5(to_hash.encode())
        yield index, result.hexdigest()
        index += 1


def main():
    # Goal: Find the index that produces the 64th valid one-time pad key
    KEYS_NEEDED = 64
    LOOKAHEAD_WINDOW = 1000  # Must check next 1000 hashes for quintuplet validation

    test_salt = 'abc'
    puzzle_salt = 'zpqevtbw'
    salt = puzzle_salt

    hasher = md5_hash_generator(salt)
    # Queue of candidate keys (index, character) that contain triplets
    candidate_keys = PriorityQueue()

    # Track indices where each character appears as a quintuplet (5 in a row)
    quintuplet_indices = defaultdict(list)

    valid_key_count = 0
    current_index, current_hash = next(hasher)
    candidate_keys.put((current_index, candidate_keys))

    while valid_key_count < KEYS_NEEDED:
        # Get the next candidate key to validate
        candidate_index, triplet_char = candidate_keys.get()
        validation_cutoff = candidate_index + LOOKAHEAD_WINDOW

        # Generate hashes up to 1000 indices ahead to look for quintuplets
        while current_index <= validation_cutoff:
            current_index, hash_value = next(hasher)

            # Find first triplet (3 identical characters in a row)
            triplet_match = re.search(r'((\w)\2{2})', hash_value)
            # Find all quintuplets (5 identical characters in a row)
            quintuplet_matches = re.findall(r'((\w)\2{4})', hash_value)

            if triplet_match:
                # This hash contains a triplet - add as candidate key
                first_triplet_char = triplet_match.group(0)[0]
                candidate_keys.put((current_index, first_triplet_char))

            if quintuplet_matches:
                # Record this index for quintuplet validation
                quintuplet_char = quintuplet_matches[0][0][0]
                quintuplet_indices[quintuplet_char].append(current_index)

            candidate_keys.put((current_index, hash_value))

        # Validate the candidate: does its triplet character appear as a quintuplet
        # in any of the next 1000 hashes?
        if triplet_char in quintuplet_indices.keys():
            if candidate_index < quintuplet_indices[triplet_char][-1] <= validation_cutoff:
                valid_key_count += 1

            if valid_key_count == KEYS_NEEDED:
                AoCUtils.print_solution(1, candidate_index)
                return

if __name__ == "__main__":
    main()