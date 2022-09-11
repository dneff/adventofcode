
def print_solution(x):
    print(f"The solution is: {x}")


class Particle():
    def __init__(self):
        self.id = 0
        self.acceleration = (0,0,0)
        self.velocity = (0,0,0)
        self.position = (0,0,0)
        self.delta = 0

    def move(self):
        start_distance = self.distance()
        v0 = self.acceleration[0] + self.velocity[0]
        v1 = self.acceleration[1] + self.velocity[1]
        v2 = self.acceleration[2] + self.velocity[2]
        self.velocity = (v0, v1, v2)
        p0, p1, p2 = self.position
        self.position = (p0 + v0, p1 + v1, p2 + v2)
        self.delta = self.distance() - start_distance

    def distance(self):
        return abs(self.position[0] + self.position[1] + self.position[2])


def main():
    file = open('input.txt', 'r', encoding='utf-8')
    particles = []
    for idx, line in enumerate(file.readlines()):
        p,v,a = [x.split('<')[1][:-1] for x in line.strip().split(', ')]
        satellite = Particle()
        satellite.acceleration = tuple([int(x) for x in a.split(',')])
        satellite.velocity = tuple([int(x) for x in v.split(',')])
        satellite.position = tuple([int(x) for x in p.split(',')])
        satellite.id = idx
        particles.append(satellite)

    low_delta = -1
    while low_delta < 0:
        deltas = []
        for p in particles:
            p.move()
            deltas.append(p.delta)
        low_delta = min(deltas)
    
    accel = []
    for p in particles:
        a = p.acceleration
        accel.append(abs(a[0]) + abs(a[1]) + abs(a[2]))

    print_solution(accel.index(min(accel)))


if __name__ == "__main__":
    main()
