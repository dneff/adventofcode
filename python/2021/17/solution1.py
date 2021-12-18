
def printSolution(x):
    print(f"The solution is {x}")


class Probe:
    def __init__(self):
        self.max_height = 0
        self.target = set()
        self.max_x = 0
        self.min_y = 0

    def parse_data(self, data):
        x, y = data.strip().split()[2:]
        x = x.split('=')[1].strip(',')
        y = y.split('=')[1]
        x = [int(x) for x in x.split('..')]
        y = [int(y) for y in y.split('..')]
        for t_x in range(min(x), max(x) + 1):
            for t_y in range(min(y), max(y) + 1):
                self.target.add((t_x, t_y))
        self.max_x = max(x)
        self.min_y = min(y)

    def checkShot(self, velocity):
        x, y = 0, 0
        max_height = 0
        positions = list()
        while x < self.max_x and y > self.min_y:
            x += velocity[0]
            y += velocity[1]
            positions.append((x, y))
            max_height = max(max_height, y)
            if velocity[0] > 0:
                velocity[0] -= 1
            elif velocity[0] < 0:
                velocity[0] += 1
            velocity[1] -= 1

        hit = self.target & set(positions)
        if len(hit) > 0:
            return max_height, positions[-1]
        return 0, positions[-1]

    def calibrate(self):
        pass


def main():
    test = 'target area: x=20..30, y=-10..-5'
    puzzle = 'target area: x=128..160, y=-142..-88'

    active = test

    p = Probe()
    p.parse_data(active)

    print(p.checkShot([17, -4]))

if __name__ == "__main__":
    main()