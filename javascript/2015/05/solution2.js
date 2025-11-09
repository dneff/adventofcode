/**
 * Advent of Code 2015 - Day 5, Part 2
 * https://adventofcode.com/2015/day/5
 *
 * Determines how many strings are "nice" based on the new rules.
 */

import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const INPUT_FILE = join(__dirname, '../../../aoc-data/2015/5/input');

function propertyOne(s) {
  // Checks if any pair appears twice
  for (let idx = 1; idx < s.length; idx++) {
    const pair = s.substring(idx - 1, idx + 1);
    const before = s.substring(0, idx - 1);
    const after = s.substring(idx + 1);

    if (before.includes(pair) || after.includes(pair)) {
      return true;
    }
  }
  return false;
}

function propertyTwo(s) {
  // Checks if any character repeats with a letter in between
  for (let idx = 2; idx < s.length; idx++) {
    if (s[idx] === s[idx - 2]) {
      return true;
    }
  }
  return false;
}

function solvePart2() {
  const lines = readFileSync(INPUT_FILE, 'utf-8').trim().split('\n');
  const nice = [];

  for (const line of lines) {
    const str = line.trim();
    if (propertyOne(str) && propertyTwo(str)) {
      nice.push(str);
    }
  }

  return nice.length;
}

const answer = solvePart2();
console.log(`Part 2: ${answer}`);
