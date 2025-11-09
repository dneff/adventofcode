/**
 * Advent of Code 2015 - Day 8, Part 2
 * https://adventofcode.com/2015/day/8
 *
 * Calculates the difference after re-encoding strings.
 */

import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const INPUT_FILE = join(__dirname, '../../../aoc-data/2015/8/input');

function solvePart2() {
  const lines = readFileSync(INPUT_FILE, 'utf-8').trim().split('\n');
  let diff = 0;

  for (const line of lines) {
    const original = line.trim();

    // Re-encode: escape backslashes and quotes, then wrap in quotes
    let encoded = original.replace(/\\/g, '\\\\').replace(/"/g, '\\"');
    encoded = '"' + encoded + '"';

    diff += encoded.length - original.length;
  }

  return diff;
}

const answer = solvePart2();
console.log(`Part 2: ${answer}`);
