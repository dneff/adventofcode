import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2016/16/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils

def AoCUtils.print_solution(1, x):
    print(f"The solution is: {x}")
def dataGenerator(initial_state, target_length):
    data = initial_state
    while len(data) < target_length:
        # copy data, reverse order, invert O's and 1's, join with "0"
        # repeat until data is larger than target size
        A = data
        B = A[::-1]
        B = B.replace('1', '2').replace('0', '1').replace('2', '0')
        data = A + "0" + B

    # truncate and return
    return data[:target_length]

def checksumGenerator(data):
    result = data[:]

    while len(result) % 2 == 0:
        odd = result[::2]
        even = result[1::2]
        difference = [x == y  for x,y in zip(odd, even)]
        result = ['1' if x == True else '0' for x in difference]

    return ''.join(result)

def main():
    test = {
        'init': "10000",
        'length': 20
    }

    puzzle_1 = {
        'init': "11011110011011101",
        'length': 272
    }

    puzzle_2 = {
        'init': "11011110011011101",
        'length': 35651584
    }
    

    active = puzzle_2

    data = dataGenerator(active['init'], active['length'])
    checksum = checksumGenerator(data)

    AoCUtils.print_solution(1, checksum)

if __name__ == "__main__":
    main()