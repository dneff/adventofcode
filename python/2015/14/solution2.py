import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2015/14/input')


class Reindeer:
    def __init__(self, name, fly_speed, fly_time, rest_time):
        self.name = name
        self.fly_time = fly_time
        self.fly_speed = fly_speed
        self.rest_time = rest_time
        self.cycle = fly_time + rest_time
        self.distance = 0
        self.time = 0

    def advanceTime(self, seconds):
        while seconds:
            if self.time % self.cycle < self.fly_time:
                self.distance += self.fly_speed
            self.time += 1
            seconds -= 1

    def __repr__(self):
        return f"Reindeer: name: {self.name}, time: {self.time}, distance: {self.distance}"


def solve_part2():
    lines = AoCInput.read_lines(INPUT_FILE)

    race_time = 2503

    racers = []
    scores = {}

    for line in lines:
        fly_speed, fly_time, rest_time = [int(x) for x in line.split() if x.isdigit()]
        name = line.split()[0]
        racers.append(Reindeer(name, fly_speed, fly_time, rest_time))
        scores[name] = 0

    while race_time:
        for deer in racers:
            deer.advanceTime(1)
        distances = [r.distance for r in racers]
        farthest = max(distances)
        for idx, distance in enumerate(distances):
            if distance == farthest:
                scores[racers[idx].name] += 1
        race_time -= 1

    return max(scores.values())


answer = solve_part2()
AoCUtils.print_solution(2, answer)
