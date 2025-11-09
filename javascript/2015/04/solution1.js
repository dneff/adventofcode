/**
 * Advent of Code 2015 - Day 4: The Ideal Stocking Stuffer
 * https://adventofcode.com/2015/day/4
 *
 * Finds the lowest positive number that produces an MD5 hash starting with five zeros.
 */

import { createHash } from 'crypto';
import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const INPUT_FILE = join(__dirname, '../../../aoc-data/2015/4/input');

function solvePart1() {
  const input = readFileSync(INPUT_FILE, 'utf-8').trim();
  let suffix = 0;
  let checking = true;

  while (checking) {
    const possible = input + suffix;
    const hash = createHash('md5').update(possible).digest('hex');

    if (hash.startsWith('00000')) {
      console.log(hash);
      checking = false;
      continue;
    }
    suffix++;
  }

  return suffix;
}

const answer = solvePart1();
console.log(`Part 1: ${answer}`);
