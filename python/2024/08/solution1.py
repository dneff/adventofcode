def print_solution(x):
    print(f"The solution is: {x}")


def find_manhattan_offset(node1, node2):
    """given two nodes, find the manhattan distance between them"""
    return node1[0] - node2[0], node1[1] - node2[1]


def find_antinodes(nodes, max_x, max_y):
    """given a list of nodes, find the antinodes"""
    """for all pairs of nodes, find the manhattan distance between them"""
    """then find the two nodes that are offset from each pair by the same amount"""
    antinodes = []
    for node in nodes:
        for other_node in nodes:
            if node != other_node:
                offset = find_manhattan_offset(node, other_node)
                antinode = (node[0] + offset[0], node[1] + offset[1])
                if antinode[0] > max_x or antinode[1] > max_y:
                    continue
                if antinode[0] < 0 or antinode[1] < 0:
                    continue
                if antinode not in nodes:
                    antinodes.append(antinode)
    return antinodes


def main():
    """finds solution"""
    filename = "./python/2024/input/08.txt"
    """get coordinates for each location in grid and assign char"""
    grid = {}
    nodes = {}
    empty = []
    with open(filename, "r", encoding="utf-8") as f:
        for y, line in enumerate(f.readlines()):
            for x, char in enumerate(line.strip()):
                grid[(x, y)] = char
                if char == ".":
                    empty.append((x, y))
                    continue
                if char not in nodes:
                    nodes[char] = []
                nodes[char].append((x, y))
    max_x = max(grid, key=lambda x: x[0])[0]
    max_y = max(grid, key=lambda x: x[1])[1]

    antinodes_list = []

    for node in nodes:
        antinodes = find_antinodes(nodes[node], max_x, max_y)
        antinodes_list.extend(antinodes)

    antinodes_list = set(antinodes_list)
    print_solution(len(antinodes_list))


if __name__ == "__main__":
    main()
