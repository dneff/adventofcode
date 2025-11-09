/**
 * Advent of Code 2015 - Day 1: Not Quite Lisp
 * https://adventofcode.com/2015/day/1
 *
 * Calculates the final floor Santa ends up on after following the instructions.
 * Each '(' means go up one floor, each ')' means go down one floor.
 */

import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const INPUT_FILE = join(__dirname, '../../../aoc-data/2015/1/input');

function solvePart1() {
  const instructions = readFileSync(INPUT_FILE, 'utf-8').trim();
  let floor = 0;

  const moveMap = {
    '(': 1,
    ')': -1,
  };

  for (const char of instructions) {
    floor += moveMap[char];
  }

  return floor;
}

const answer = solvePart1();
console.log(`Part 1: ${answer}`);
