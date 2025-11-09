/**
 * Advent of Code 2015 - Day 14: Reindeer Olympics
 * https://adventofcode.com/2015/day/14
 *
 * Determines which reindeer wins using the points system.
 */

import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const INPUT_FILE = join(__dirname, '../../../aoc-data/2015/14/input');

class Reindeer {
  constructor(name, flySpeed, flyTime, restTime) {
    this.name = name;
    this.flyTime = flyTime;
    this.flySpeed = flySpeed;
    this.restTime = restTime;
    this.cycle = flyTime + restTime;
    this.distance = 0;
    this.time = 0;
  }

  advanceTime(seconds) {
    while (seconds > 0) {
      if (this.time % this.cycle < this.flyTime) {
        this.distance += this.flySpeed;
      }
      this.time += 1;
      seconds -= 1;
    }
  }
}

function solvePart2() {
  const lines = readFileSync(INPUT_FILE, 'utf-8').trim().split('\n');

  let raceTime = 2503;
  const racers = [];
  const scores = {};

  for (const line of lines) {
    const numbers = line.split(' ').filter(x => /^\d+$/.test(x)).map(Number);
    const [flySpeed, flyTime, restTime] = numbers;
    const name = line.split(' ')[0];
    racers.push(new Reindeer(name, flySpeed, flyTime, restTime));
    scores[name] = 0;
  }

  while (raceTime > 0) {
    for (const deer of racers) {
      deer.advanceTime(1);
    }
    const distances = racers.map(r => r.distance);
    const farthest = Math.max(...distances);
    for (let idx = 0; idx < distances.length; idx++) {
      if (distances[idx] === farthest) {
        scores[racers[idx].name] += 1;
      }
    }
    raceTime -= 1;
  }

  return Math.max(...Object.values(scores));
}

const answer = solvePart2();
console.log(`Part 2: ${answer}`);
