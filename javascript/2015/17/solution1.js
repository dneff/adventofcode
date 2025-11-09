/**
 * Advent of Code 2015 - Day 17: No Such Thing as Too Much
 * https://adventofcode.com/2015/day/17
 *
 * Finds how many combinations of containers can hold exactly 150 liters of eggnog.
 */

import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const INPUT_FILE = join(__dirname, '../../../aoc-data/2015/17/input');

function solvePart1() {
  const lines = readFileSync(INPUT_FILE, 'utf-8').trim().split('\n');

  const eggnog = 150;
  const containers = lines.map(Number);

  let validCombos = 0;

  for (let x = 1; x < 2 ** containers.length; x++) {
    const mask = x.toString(2).padStart(containers.length, '0').split('').map(Number);
    const containerValue = mask.reduce((sum, m, i) => sum + m * containers[i], 0);

    if (containerValue === eggnog) {
      validCombos += 1;
    }
  }

  return validCombos;
}

const answer = solvePart1();
console.log(`Part 1: ${answer}`);
