
def print_solution(x):
    """ prints solution """
    print(f"The solution is: {x}")

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
    file = open('input.txt', 'r', encoding='utf-8')

    node_hash = {}

    # creates nodes without relationships
    for line in file.readlines():
        node_name, node_score = line.strip().split()[:2]
        node_score = int(node_score.strip('()'))
        node_hash[node_name] = Node()
        node_hash[node_name].name = node_name
        node_hash[node_name].score = node_score

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
    for k,v in node_hash.items():
        if v.parent == None:
            print_solution(v.name)

if __name__ == "__main__":
    main()
