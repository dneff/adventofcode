"""
Advent of Code 2017 - Day 20: Particle Swarm (Part 2)

In Part 2, particles at the same position collide and are removed from the simulation.
After running the simulation until all collisions have resolved, count how many
particles remain.

The simulation runs for a fixed number of steps (200), which is sufficient for
all collisions to occur in the input data.
"""
import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/20/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402
from collections import defaultdict  # noqa: E402


class Particle():
    """Represents a particle with position, velocity, and acceleration in 3D space."""
    def __init__(self):
        self.acceleration = (0, 0, 0)
        self.velocity = (0, 0, 0)
        self.position = (0, 0, 0)

    def move_old(self):
        """Legacy move method (unused)."""
        v0 = self.acceleration[0] + self.velocity[0]
        v1 = self.acceleration[1] + self.velocity[1]
        v2 = self.acceleration[2] + self.velocity[2]
        self.velocity = (v0, v1, v2)
        p0, p1, p2 = self.position
        self.position = (p0 + v0, p1 + v1, p2 + v2)

    def move(self):
        """Update velocity by acceleration, then update position by velocity."""
        a, v, p = list(self.acceleration), list(self.velocity), list(self.position)
        for i in range(3):
            v[i] += a[i]
            p[i] += v[i]
        self.acceleration = tuple(a)
        self.velocity = tuple(v)
        self.position = tuple(p)


def main():
    """Simulate particle collisions and count remaining particles."""
    lines = AoCInput.read_lines(INPUT_FILE)
    particles = {}

    # Parse particle data
    for idx, line in enumerate(lines):
        p, v, a = [x.split('<')[1][:-1] for x in line.strip().split(', ')]
        particle = Particle()
        particle.acceleration = tuple([int(x) for x in a.split(',')])
        particle.velocity = tuple([int(x) for x in v.split(',')])
        particle.position = tuple([int(x) for x in p.split(',')])
        particle.id = idx
        particles[idx] = particle

    # Simulate for enough steps to resolve all collisions
    positions = defaultdict(list)
    for steps in range(200):
        # Move all particles
        for idx, p in particles.items():
            p.move()
            positions[p.position].append(idx)

        # Remove particles that collided (same position)
        for particle_ids_at_position in positions.values():
            if len(particle_ids_at_position) > 1:
                for particle_id in particle_ids_at_position:
                    del particles[particle_id]
        positions.clear()

    AoCUtils.print_solution(2, len(particles))


if __name__ == "__main__":
    main()
