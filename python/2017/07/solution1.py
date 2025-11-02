import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/7/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


class Node():
    def __init__(self):
        self.name = None
        self.parent = None
        self.value = 0
        self.children = []

    def __getitem__(self, i):
        return self.children[i]


def main():
    """ calculates solution """
    lines = AoCInput.read_lines(INPUT_FILE)

    node_hash = {}

    # creates nodes without relationships
    for line in lines:
        node_name, node_score = line.strip().split()[:2]
        node_score = int(node_score.strip('()'))
        node_hash[node_name] = Node()
        node_hash[node_name].name = node_name
        node_hash[node_name].score = node_score

    # create parent/child relationships
    for line in lines:
        values = line.strip().split()
        if len(values) > 3:
            parent = values[0]
            for child in values[3:]:
                child = child.strip(',')
                node_hash[parent].children.append(node_hash[child])
                node_hash[child].parent = node_hash[parent]

    # look for node.parent = None
    for k,v in node_hash.items():
        if v.parent == None:
            AoCUtils.print_solution(1, v.name)

if __name__ == "__main__":
    main()
