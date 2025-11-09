/**
 * Advent of Code 2015 - Day 14: Reindeer Olympics
 * https://adventofcode.com/2015/day/14
 *
 * Determines which reindeer travels the farthest in 2503 seconds.
 */

import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const INPUT_FILE = join(__dirname, '../../../aoc-data/2015/14/input');

class Reindeer {
  constructor(flySpeed, flyTime, restTime) {
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

function solvePart1() {
  const lines = readFileSync(INPUT_FILE, 'utf-8').trim().split('\n');

  const raceTime = 2503;
  let maxDistance = 0;

  for (const line of lines) {
    const numbers = line.split(' ').filter(x => /^\d+$/.test(x)).map(Number);
    const [flySpeed, flyTime, restTime] = numbers;
    const reindeer = new Reindeer(flySpeed, flyTime, restTime);
    reindeer.advanceTime(raceTime);
    maxDistance = Math.max(maxDistance, reindeer.distance);
  }

  return maxDistance;
}

const answer = solvePart1();
console.log(`Part 1: ${answer}`);
