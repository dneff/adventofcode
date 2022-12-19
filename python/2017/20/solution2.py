from collections import defaultdict

def print_solution(x):
    print(f"The solution is: {x}")


class Particle():
    def __init__(self):
        self.acceleration = (0,0,0)
        self.velocity = (0,0,0)
        self.position = (0,0,0)

    def move_old(self):
        v0 = self.acceleration[0] + self.velocity[0]
        v1 = self.acceleration[1] + self.velocity[1]
        v2 = self.acceleration[2] + self.velocity[2]
        self.velocity = (v0, v1, v2)
        p0, p1, p2 = self.position
        self.position = (p0 + v0, p1 + v1, p2 + v2)

    def move(self):
        a,v,p = list(self.acceleration), list(self.velocity), list(self.position)
        for i in range(3):
            v[i] += a[i]
            p[i] += v[i]
        self.acceleration = tuple(a)
        self.velocity = tuple(v)
        self.position = tuple(p)


def main():
    file = open('input.txt', 'r', encoding='utf-8')
    particles = {}
    for idx, line in enumerate(file.readlines()):
        p,v,a = [x.split('<')[1][:-1] for x in line.strip().split(', ')]
        satellite = Particle()
        satellite.acceleration = tuple([int(x) for x in a.split(',')])
        satellite.velocity = tuple([int(x) for x in v.split(',')])
        satellite.position = tuple([int(x) for x in p.split(',')])
        satellite.id = idx
        particles[idx] = satellite


    positions = defaultdict(list)
    for steps in range(200):    
        for idx, p in particles.items():
            p.move()
            positions[p.position].append(idx)
            
        for v in positions.values():
            if len(v) > 1:
                for i in v:
                    del particles[i]
        positions.clear()

    print_solution(len(particles))


if __name__ == "__main__":
    main()
