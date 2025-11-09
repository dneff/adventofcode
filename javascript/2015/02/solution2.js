/**
 * Advent of Code 2015 - Day 2, Part 2
 * https://adventofcode.com/2015/day/2
 *
 * Calculates the total ribbon needed for all presents.
 */

import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const INPUT_FILE = join(__dirname, '../../../aoc-data/2015/2/input');

function getRibbon(length, width, height) {
  const perimeters = [length + width, width + height, height + length];
  const ribbon = 2 * Math.min(...perimeters);
  return ribbon;
}

function getBow(length, width, height) {
  return length * width * height;
}

function solvePart2() {
  const lines = readFileSync(INPUT_FILE, 'utf-8').trim().split('\n');
  let totalRibbon = 0;

  for (const line of lines) {
    const [l, w, h] = line.trim().split('x').map(Number);
    totalRibbon += getRibbon(l, w, h);
    totalRibbon += getBow(l, w, h);
  }

  return totalRibbon;
}

const answer = solvePart2();
console.log(`Part 2: ${answer}`);
