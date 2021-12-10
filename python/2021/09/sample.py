from collections import deque

with open('input.txt') as fh:
    data = fh.read()

grid = {}
for y, line in enumerate(data.split()):
    for x, c in enumerate(line):
        grid[complex(x, -y)] = int(c)

def iter_neighbors(coord, grid=grid):
    for delta in [1, 0+1j, -1, 0-1j]:
        p = grid.get(coord + delta)
        if p is not None:
            yield p

# part 1

total_risk = 0
for (coord, p) in grid.items():
    if p < min(iter_neighbors(coord)):
        total_risk += p + 1
part_1 = total_risk
print('part_1 =', part_1)


# part 2

def bfs(p, space):
    q = deque([p])
    visited = {p}
    while q:
        c = q.popleft()
        for delta in [1, 0+1j, -1, 0-1j]:
            n = c + delta
            if n in visited:
                continue
            try:
                space.remove(n)
            except KeyError:
                continue
            visited.add(n)
            q.append(n)
    return len(visited)


space = {k for k, v in grid.items() if v != 9}
basins = []
while space:
    p = space.pop()
    basins.append(bfs(p, space))

part_2 = 1
for x in sorted(basins)[-3:]:
    part_2 *= x
print('part_2=', part_2)