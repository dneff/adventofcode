import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, "../../../../aoc-data/2016/14/input")
sys.path.append(os.path.join(SCRIPT_DIR, "../../"))

from aoc_helpers import AoCInput, AoCUtils

from hashlib import md5
from multiprocessing import Pool


def compute_stretched_hash(args):
    """
    Compute a stretched MD5 hash for the given salt and index.

    Key stretching makes hash generation more secure by requiring additional
    computational work. After computing the initial MD5 hash of salt+index,
    we apply MD5 an additional 2016 times (2017 total MD5 operations).

    Args:
        args: Tuple of (salt, index)

    Returns:
        tuple: (index, hash_string) - The index and stretched MD5 hash
    """
    salt, index = args
    # Initial input: salt + index
    result = salt + str(index)

    # Key stretching: Apply MD5 2017 times total
    for _ in range(2017):
        result = md5(result.encode()).hexdigest()

    return index, result


def find_triplet(hash_str):
    """
    Find the first character that appears three times in a row.

    Args:
        hash_str: The hash string to search

    Returns:
        str or None: The character that appears in triplet, or None if not found
    """
    for i in range(len(hash_str) - 2):
        if hash_str[i] == hash_str[i + 1] == hash_str[i + 2]:
            return hash_str[i]
    return None


def has_quintuplet(hash_str, char):
    """
    Check if a character appears five times in a row in the hash.

    Args:
        hash_str: The hash string to search
        char: The character to look for

    Returns:
        bool: True if the character appears 5 times consecutively
    """
    target = char * 5
    return target in hash_str


def main():
    # Goal: Find the index that produces the 64th valid one-time pad key
    # using key stretching (2017 total MD5 operations per hash)
    KEYS_NEEDED = 64
    LOOKAHEAD_WINDOW = 1000  # Must check next 1000 hashes for quintuplet validation

    test_salt = "abc"
    puzzle_salt = "zpqevtbw"
    salt = puzzle_salt

    # Pre-compute a large batch of hashes in parallel
    # We need to compute at least up to where the 64th key might be (around 23500)
    MAX_INDEX = 24000
    with Pool() as pool:
        results = pool.map(
            compute_stretched_hash, [(salt, i) for i in range(MAX_INDEX)], chunksize=100
        )

    # Store results in a dict for fast lookup
    hashes = {idx: hash_val for idx, hash_val in results}

    valid_key_count = 0
    index = 0

    while valid_key_count < KEYS_NEEDED and index < MAX_INDEX:
        current_hash = hashes[index]
        triplet_char = find_triplet(current_hash)

        if triplet_char:
            # Found a triplet - check next 1000 hashes for matching quintuplet
            for lookahead_index in range(
                index + 1, min(index + LOOKAHEAD_WINDOW + 1, MAX_INDEX)
            ):
                lookahead_hash = hashes[lookahead_index]

                if has_quintuplet(lookahead_hash, triplet_char):
                    # Valid key found!
                    valid_key_count += 1

                    if valid_key_count == KEYS_NEEDED:
                        AoCUtils.print_solution(2, index)
                        return

                    # Move to next index after finding a valid key
                    break

        index += 1


if __name__ == "__main__":
    main()
