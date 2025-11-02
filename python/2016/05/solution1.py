import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2016/5/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils
import string
import hashlib

def main():
    seed = AoCInput.read_lines(INPUT_FILE)[0].strip()
    index = 0
    hashed = []
    while len(hashed) < 8:
        h = hashlib.md5()
        h.update(str.encode(seed+str(index)))
        out = str(h.hexdigest())
        if out[:5] == '00000':
            hashed.append(out[5])
            print(".",)
        index += 1
    
    AoCUtils.print_solution(1, ''.join(hashed))

if __name__ == "__main__":
    main()