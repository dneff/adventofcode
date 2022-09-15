from collections import defaultdict


def print_solution(x):
    """formats input for printing"""
    print(f"The solution is: {x}")


class GridBug():
    """simulated virus"""
    def __init__(self):
        self.next = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        self.heading = 0
        self.location = (0, 0)
        self.infection_count = 0

    def left(self):
        self.heading = (self.heading - 1) % 4

    def right(self):
        self.heading = (self.heading + 1) % 4

    def move(self):
        x, y = [a+b for a, b in zip(self.location, self.next[self.heading])]
        self.location = (x, y)

    def burst(self, node_status):
        if self.location in node_status:
            self.right()
        else:
            self.left()

        if self.location in node_status:
            del node_status[self.location]
        else:
            node_status[self.location] += 1
            self.infection_count += 1

        self.move()


def main():
    file = open('input.txt', 'r', encoding='utf-8')
    node_status = defaultdict(int)

    max_x = 0
    max_y = 0
    for y, line in enumerate(file.readlines()):
        max_y = max(y, max_y)
        for x, node in enumerate(line):
            max_x = max(x, max_x)
            if node == '#':
                node_status[(x, y)] += 1

    virus = GridBug()
    virus.location = (max_x//2, max_y//2)

    for _ in range(10000):
        virus.burst(node_status)

    print_solution(virus.infection_count)


if __name__ == "__main__":
    main()
