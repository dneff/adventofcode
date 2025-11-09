/**
 * Advent of Code 2015 - Day 13: Knights of the Dinner Table
 * https://adventofcode.com/2015/day/13
 *
 * Finds the optimal seating arrangement including yourself (neutral happiness).
 */

import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const INPUT_FILE = join(__dirname, '../../../aoc-data/2015/13/input');

function* permutations(arr) {
  if (arr.length <= 1) {
    yield arr;
  } else {
    for (let i = 0; i < arr.length; i++) {
      const rest = [...arr.slice(0, i), ...arr.slice(i + 1)];
      for (const perm of permutations(rest)) {
        yield [arr[i], ...perm];
      }
    }
  }
}

function solvePart2() {
  const lines = readFileSync(INPUT_FILE, 'utf-8').trim().split('\n');

  const happiness = {};

  for (let line of lines) {
    line = line.trim().replace('.', '');
    let subject, difference, guest;

    if (line.includes('would lose')) {
      const parts = line.replace('would lose ', '-').split(' ');
      subject = parts[0];
      difference = parseInt(parts[1], 10);
      guest = parts[parts.length - 1];
    } else {
      const parts = line.replace('would gain ', '').split(' ');
      subject = parts[0];
      difference = parseInt(parts[1], 10);
      guest = parts[parts.length - 1];
    }

    if (!happiness[subject]) {
      happiness[subject] = {};
    }
    happiness[subject][guest] = difference;
  }

  // Add myself with neutral happiness
  const guests = Object.keys(happiness);
  happiness['me'] = {};
  for (const guest of guests) {
    happiness['me'][guest] = 0;
    happiness[guest]['me'] = 0;
  }

  const allGuests = Object.keys(happiness);
  let mostHappy = 0;

  for (const seating of permutations(allGuests)) {
    let tableHappiness = 0;
    for (let i = 0; i < seating.length - 1; i++) {
      const x = seating[i];
      const y = seating[i + 1];
      tableHappiness += happiness[x][y] + happiness[y][x];
    }
    // Connect first and last
    tableHappiness += happiness[seating[0]][seating[seating.length - 1]];
    tableHappiness += happiness[seating[seating.length - 1]][seating[0]];
    mostHappy = Math.max(mostHappy, tableHappiness);
  }

  return mostHappy;
}

const answer = solvePart2();
console.log(`Part 2: ${answer}`);
