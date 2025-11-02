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
def AoCUtils.print_solution(2, x):
    print(f"The solution is: {x}")
def hashGenerator(salt):
    num = 0
    while True:
        to_hash = salt + str(num)
        result = md5(to_hash.encode())

        for _ in range(2016):
            result = md5(result.hexdigest().encode())

        yield num, result.hexdigest()
        num += 1

def main():
    keys_needed = 64

    test_salt = 'abc'
    puzzle_salt = 'zpqevtbw'
    salt = puzzle_salt
    
    hasher = hashGenerator(salt)
    possible_keys = PriorityQueue()
    
    len_5 = defaultdict(list)

    key_count = 0
    hash_idx, possible_key = next(hasher)
    possible_keys.put((hash_idx, possible_key))

    while key_count < keys_needed:
        possible_idx, possible_key = possible_keys.get()
        cutoff = possible_idx + 1000
        while hash_idx <= cutoff:
            hash_idx, h = next(hasher)
            three = re.search(r'((\w)\2{2})', h)
            five = re.findall(r'((\w)\2{4})', h)
            if three:
                possible_keys.put((hash_idx, three.group(0)[1]))
            if five:
                len_5[five[0][0][0]].append(hash_idx)
            possible_keys.put((hash_idx, h))

        if possible_key in len_5.keys():
            if possible_idx < len_5[possible_key][-1] <= cutoff:
                key_count += 1

            if key_count == keys_needed:
                AoCUtils.print_solution(2, possible_idx)

if __name__ == "__main__":
    main()