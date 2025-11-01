import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2015/14/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


class Reindeer:
    def __init__(self, fly_speed, fly_time, rest_time):
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
        return f"Reindeer: time: {self.time}, distance: {self.distance}"


def solve_part1():
    lines = AoCInput.read_lines(INPUT_FILE)

    race_time = 2503

    max_distance = 0
    for line in lines:
        fly_speed, fly_time, rest_time = [int(x) for x in line.split() if x.isdigit()]
        reindeer = Reindeer(fly_speed, fly_time, rest_time)
        reindeer.advanceTime(race_time)
        max_distance = max(max_distance, reindeer.distance)

    return max_distance


answer = solve_part1()
AoCUtils.print_solution(1, answer)
