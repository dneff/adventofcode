/**
 * Advent of Code 2015 - Day 1, Part 2
 * https://adventofcode.com/2015/day/1
 *
 * Finds the position of the first character that causes Santa to enter the basement (floor -1).
 */

import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const INPUT_FILE = join(__dirname, '../../../aoc-data/2015/1/input');

function findBasementEntryPosition() {
  const instructions = readFileSync(INPUT_FILE, 'utf-8').trim();
  let currentFloor = 0;
  const moveMap = { '(': 1, ')': -1 };

  for (let idx = 0; idx < instructions.length; idx++) {
    currentFloor += moveMap[instructions[idx]];
    if (currentFloor === -1) {
      return idx + 1;
    }
  }

  return -1;
}

const answer = findBasementEntryPosition();
console.log(`Part 2: ${answer}`);
