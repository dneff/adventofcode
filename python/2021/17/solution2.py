import math

def printSolution(x):
    print(f"The solution is {x}")


class Probe:
    def __init__(self):
        self.max_height = 0
        self.target = set()
        self.range_x =  (0,0)
        self.range_y =  (0,0)
        self.center = (0,0)

    def parse_data(self, data):
        x, y = data.strip().split()[2:]
        x = x.split('=')[1].strip(',')
        y = y.split('=')[1]
        x = [int(x) for x in x.split('..')]
        y = [int(y) for y in y.split('..')]
        for t_x in range(min(x), max(x) + 1):
            for t_y in range(min(y), max(y) + 1):
                self.target.add((t_x, t_y))
        self.range_x = (min(x), max(x))
        self.range_y = (min(y), max(y))
        self.center = (sum(x)//2, sum(y)//2)

    def checkShot(self, velocity):
        velocity = list(velocity)
        x, y = 0, 0
        max_height = 0
        positions = list()
        while x < max(self.range_x) and y > min(self.range_y):
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
            return True
        return False

    def calibrate(self):
        # y arc is perfect parabola to 0, then y velocity + 1 to target
        y_velocity = abs(min(self.range_y)) - 1
        y_height = (y_velocity * (y_velocity + 1))//2
        x_velocity = int(math.sqrt(max(self.range_x) * 2))
        return (x_velocity, y_velocity)


def main():
    test = 'target area: x=20..30, y=-10..-5'
    puzzle = 'target area: x=128..160, y=-142..-88'

    active = puzzle

    p = Probe()
    p.parse_data(active)
    print(p.calibrate())
    x_vel_min, y_vel_max = p.calibrate()

    hits = set()
    for y in range(min(p.range_y) - 1, y_vel_max + 1):
        for x in range(x_vel_min - 1, max(p.range_x) + 1):
            if p.checkShot((x,y)):
                hits.add((x,y))

    printSolution(len(hits))
    
if __name__ == "__main__":
    main()