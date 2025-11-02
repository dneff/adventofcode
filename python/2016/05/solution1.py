import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2016/5/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils
import hashlib
from multiprocessing import Pool, cpu_count

def find_hashes_in_range(args):
    """
    Worker function to find hashes with five leading zeros in a given range.
    Returns list of (index, password_char) tuples.
    """
    door_id, start, end = args
    results = []

    for index in range(start, end):
        digest = hashlib.md5(f"{door_id}{index}".encode()).digest()

        # Check if first 2 bytes are zero and first nibble of 3rd byte is zero
        if digest[0] == 0 and digest[1] == 0 and digest[2] < 16:
            hex_hash = digest.hex()
            results.append((index, hex_hash[5]))

    return results

def main():
    """
    Advent of Code 2016 - Day 5: How About a Nice Game of Chess?

    Find an 8-character password by hashing a door ID with incrementing indices.
    For each hash that starts with five zeros (00000), the sixth character becomes
    the next character in the password.

    Uses multiprocessing to parallelize the MD5 computation across CPU cores.
    """
    # Read the door ID from input file
    door_id = AoCInput.read_lines(INPUT_FILE)[0].strip()

    # Use multiprocessing to search in parallel
    num_cores = cpu_count()
    chunk_size = 100000  # Process 100k indices per chunk

    password_chars = []
    current_index = 0

    with Pool(num_cores) as pool:
        while len(password_chars) < 8:
            # Create work chunks for each core
            chunks = [
                (door_id, current_index + i * chunk_size, current_index + (i + 1) * chunk_size)
                for i in range(num_cores)
            ]

            # Process chunks in parallel
            results = pool.map(find_hashes_in_range, chunks)

            # Collect all results and sort by index to maintain order
            all_matches = []
            for chunk_results in results:
                all_matches.extend(chunk_results)

            all_matches.sort(key=lambda x: x[0])

            # Add password characters in order until we have 8
            for _, char in all_matches:
                if len(password_chars) < 8:
                    password_chars.append(char)
                else:
                    break

            # Move to next batch
            current_index += num_cores * chunk_size

    # Join all password characters to form the final 8-character password
    password = ''.join(password_chars)
    AoCUtils.print_solution(1, password)

if __name__ == "__main__":
    main()