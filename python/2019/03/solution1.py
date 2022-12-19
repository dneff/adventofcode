
def endPoint(loc, run):
    x, y = loc
    distance = int(run[1:])

    if run[0] == 'U':
        y += distance
    elif run[0] == 'D':
        y -= distance
    elif run[0] == 'L':
        x -= distance
    elif run[0] == 'R':
        x += distance

    return (x, y)

def findPoints(path):
    pos = [0, 0]
    for i in path:
        for _ in range(int(i[1:])):
            if i[0] == 'L':
                pos[0] += -1
            elif i[0] == 'R':
                pos[0] += 1
            elif i[0] == 'U':
                pos[1] += 1
            elif i[0] == 'D':
                pos[1] += -1

            yield tuple(pos)

def main():
    with open('input1.txt', 'r') as file:
        path_a = file.readline().strip().split(',')
        path_b = file.readline().strip().split(',')

    points_a = list(findPoints(path_a))
    points_b = list(findPoints(path_b))

    intersections = set(points_a) & set(points_b)

    solution = min([abs(x) + abs(y) for x, y in intersections])
    print(f"The solution is: {solution}")

    lengths = []
    for intersect in intersections:
        dist = []
        for points in points_a, points_b:
            dist.append(points.index(intersect))
        
        lengths.append(sum(dist) + 2)
        
    print(f"The second solution is: {min(lengths)}")

if __name__ == "__main__":
    main()