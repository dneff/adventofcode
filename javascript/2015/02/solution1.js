/**
 * Advent of Code 2015 - Day 2: I Was Told There Would Be No Math
 * https://adventofcode.com/2015/day/2
 *
 * Calculates the total wrapping paper needed for all presents.
 */

import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const INPUT_FILE = join(__dirname, '../../../aoc-data/2015/2/input');

function getWrapping(length, width, height) {
  const sides = [length * width, width * height, height * length];
  const wrapping = 2 * sides.reduce((sum, side) => sum + side, 0);
  const slack = Math.min(...sides);
  return wrapping + slack;
}

function solvePart1() {
  const lines = readFileSync(INPUT_FILE, 'utf-8').trim().split('\n');
  let totalWrapping = 0;

  for (const line of lines) {
    const [l, w, h] = line.trim().split('x').map(Number);
    totalWrapping += getWrapping(l, w, h);
  }

  return totalWrapping;
}

const answer = solvePart1();
console.log(`Part 1: ${answer}`);
