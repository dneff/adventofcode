from collections import defaultdict


def print_solution(x):
    """ prints solution """
    print(f"The solution is: {x}")


class Node():
    def __init__(self):
        self.name = None
        self.parent = None
        self.weight = 0
        self.children = []


    def __getitem__(self, i):
        return self.children[i]


def correctBalance(node):
    """ verify balance of each sub node. If imbalanced, correct and continue. """
    child_sum = 0
    child_weights = defaultdict(list)
    if len(node.children) == 0:
        return node.weight
        
    for child in node.children:
        balance = correctBalance(child)
        child_weights[balance].append(child)
        child_sum += balance

    if len(set(child_weights.keys())) > 1:
        imbalanced = None
        balanced = None
        imbalanced_node = None
        for k, v in child_weights.items():
            if len(v) == 1:
                imbalanced = k
                imbalanced_node = v[0]
            else:
                balanced = k
        correction = balanced - imbalanced
        imbalanced_node.weight += correction
        print_solution(imbalanced_node.weight)
        return correctBalance(node)

    total_weight = child_sum + node.weight
    return total_weight


def main():
    """ calculates solution """
    file = open('input.txt', 'r', encoding='utf-8')

    node_hash = {}

    # creates nodes without relationships
    for line in file.readlines():
        node_name, node_weight = line.strip().split()[:2]
        node_weight = int(node_weight.strip('()'))
        node_hash[node_name] = Node()
        node_hash[node_name].name = node_name
        node_hash[node_name].weight = node_weight

    # second pass for relationships
    file.seek(0)

    # create parent/child relationships
    for line in file.readlines():
        values = line.strip().split()
        if len(values) > 3:
            parent = values[0]
            for child in values[3:]:
                child = child.strip(',')
                node_hash[parent].children.append(node_hash[child])
                node_hash[child].parent = node_hash[parent]

    # look for node.parent = None
    root = None
    for k,v in node_hash.items():
        if v.parent == None:
            root = v
            break

    # correct balance if necessary
    correctBalance(root)


if __name__ == "__main__":
    main()
