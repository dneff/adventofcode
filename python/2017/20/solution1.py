"""
Advent of Code 2017 - Day 20: Particle Swarm (Part 1)

Particles move in 3D space with position, velocity, and acceleration vectors.
Each tick:
1. Velocity increases by acceleration
2. Position increases by velocity

The challenge is to determine which particle will stay closest to position <0, 0, 0>
in the long term, as measured by Manhattan distance (sum of absolute coordinates).

The answer is the ID of the particle that remains closest over infinite time.
"""
import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/20/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402


class Particle():
    """Represents a particle with position, velocity, and acceleration in 3D space."""
    def __init__(self):
        self.id = 0
        self.acceleration = (0, 0, 0)
        self.velocity = (0, 0, 0)
        self.position = (0, 0, 0)
        self.delta = 0  # Change in distance from origin after last move

    def move(self):
        """Update velocity by acceleration, then update position by velocity."""
        start_distance = self.manhattan_distance()

        # Update velocity by adding acceleration
        v0 = self.acceleration[0] + self.velocity[0]
        v1 = self.acceleration[1] + self.velocity[1]
        v2 = self.acceleration[2] + self.velocity[2]
        self.velocity = (v0, v1, v2)

        # Update position by adding velocity
        p0, p1, p2 = self.position
        self.position = (p0 + v0, p1 + v1, p2 + v2)

        # Track how distance changed
        self.delta = self.manhattan_distance() - start_distance

    def manhattan_distance(self):
        """Calculate Manhattan distance from origin."""
        return abs(self.position[0] + self.position[1] + self.position[2])


def main():
    """Find which particle stays closest to the origin in the long term."""
    lines = AoCInput.read_lines(INPUT_FILE)
    particles = []

    # Parse particle data
    for idx, line in enumerate(lines):
        p, v, a = [x.split('<')[1][:-1] for x in line.strip().split(', ')]
        particle = Particle()
        particle.acceleration = tuple([int(x) for x in a.split(',')])
        particle.velocity = tuple([int(x) for x in v.split(',')])
        particle.position = tuple([int(x) for x in p.split(',')])
        particle.id = idx
        particles.append(particle)

    # Simulate until all particles are moving away from origin
    low_delta = -1
    while low_delta < 0:
        deltas = []
        for p in particles:
            p.move()
            deltas.append(p.delta)
        low_delta = min(deltas)

    # The particle with lowest acceleration magnitude will be closest long-term
    acceleration_magnitudes = []
    for p in particles:
        a = p.acceleration
        acceleration_magnitudes.append(abs(a[0]) + abs(a[1]) + abs(a[2]))

    AoCUtils.print_solution(1, acceleration_magnitudes.index(min(acceleration_magnitudes)))


if __name__ == "__main__":
    main()
