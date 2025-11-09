/**
 * Advent of Code 2015 - Day 25: Let It Snow
 * https://adventofcode.com/2015/day/25
 *
 * Generate a code at a specific row and column position.
 */

import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const INPUT_FILE = join(__dirname, '../../../aoc-data/2015/25/input');

function nextCode(x) {
  if (x === 0) {
    return 20151125;
  } else {
    return (x * 252533) % 33554393;
  }
}

function getIterations(row, col) {
  const maxRow = row + col - 1;
  let iterations = 0;
  for (let x = 0; x < maxRow; x++) {
    iterations += x;
  }
  iterations += col;
  return iterations;
}

function solvePart1() {
  const codeLoc = [2978, 3083];

  let code = 0;
  const iterations = getIterations(...codeLoc);
  for (let i = 0; i < iterations; i++) {
    code = nextCode(code);
  }

  return code;
}

const answer = solvePart1();
console.log(`Part 1: ${answer}`);
