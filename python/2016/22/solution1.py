from collections import defaultdict

def printSolution(x):
    print(f"The solution is {x}")

def main():

    nodes = defaultdict(list)

    f = open('input.txt', 'r')
    for line in f.readlines():
        node, size, used, available, usage_pct = line.strip().split()
        _, x, y = node.split('-')
        x, y = x[1:], y[1:]
        if len(y) == 1:
            y = '0' + y
        node_id = x + y
        nodes[node_id] = [int(size[:-1]), int(used[:-1]), int(available[:-1]), int(usage_pct[:-1])]

    valid_pairs = 0
    for A in nodes.keys():
        for B in nodes.keys():
            if A == B:
                continue
            if nodes[A][1] == 0:
                continue
            if nodes[A][1] <= nodes[B][2]:
                valid_pairs += 1
    printSolution(valid_pairs)

if __name__ == "__main__":
    main()