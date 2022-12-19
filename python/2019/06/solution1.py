
def objectDistance(graph, src, dest):
    objects = [src]
    if graph[src] == dest:
        objects.append(dest)
    else:
        objects.extend(objectDistance(graph, graph[src], dest))
    return objects

def main():
    graph = {}
    with open('input1.txt', 'r') as file:
        for line in file.readlines():
            pair = line.strip().split(')')
            graph[pair[1]] = pair[0]

    orbits = 0
    for k in graph.keys():
        orbits += len(objectDistance(graph, k, 'COM')) - 1
    print(f"The total number of orbits is {orbits}")

    you_path = objectDistance(graph, 'YOU', 'COM')
    santa_path = objectDistance(graph, 'SAN', 'COM')

    while you_path[-2] == santa_path[-2]:
        you_path.pop()
        santa_path.pop()

    # transfers equals path lengths minus YOU minus SAN minus two as we're counting edges, not nodes 
    print(f"The number of transfers from YOU->SAN: {len(you_path) + len(santa_path) - 4}")


if __name__ == "__main__":
    main()