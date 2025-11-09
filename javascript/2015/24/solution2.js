/**
 * Advent of Code 2015 - Day 24: It Hangs in the Balance
 * https://adventofcode.com/2015/day/24
 *
 * Find the optimal package arrangement to balance the sleigh (4 groups).
 */

import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const INPUT_FILE = join(__dirname, '../../../aoc-data/2015/24/input');

function* combinations(array, size) {
  if (size === 0) {
    yield [];
    return;
  }
  if (size > array.length) {
    return;
  }
  for (let i = 0; i <= array.length - size; i++) {
    const head = array[i];
    const tail = array.slice(i + 1);
    for (const combo of combinations(tail, size - 1)) {
      yield [head, ...combo];
    }
  }
}

function solvePart2() {
  const lines = readFileSync(INPUT_FILE, 'utf-8').trim().split('\n');
  const packageWeights = lines.map(Number);

  const targetWeight = Math.floor(packageWeights.reduce((a, b) => a + b, 0) / 4);

  let maxPackagesInGroup = 1;
  while (packageWeights.slice(0, maxPackagesInGroup).reduce((a, b) => a + b, 0) <= targetWeight) {
    maxPackagesInGroup++;
  }

  let minPackagesInGroup = 1;
  while (packageWeights.slice(-minPackagesInGroup).reduce((a, b) => a + b, 0) <= targetWeight) {
    minPackagesInGroup++;
  }

  for (let groupSize = minPackagesInGroup; groupSize <= maxPackagesInGroup; groupSize++) {
    let minQuantumEntanglement = null;

    for (const combo of combinations(packageWeights, groupSize)) {
      if (combo.reduce((a, b) => a + b, 0) === targetWeight) {
        const qe = combo.reduce((a, b) => a * b, 1);

        if (minQuantumEntanglement === null || qe < minQuantumEntanglement) {
          minQuantumEntanglement = qe;
        }
      }
    }

    if (minQuantumEntanglement !== null) {
      return minQuantumEntanglement;
    }
  }

  return null;
}

const answer = solvePart2();
console.log(`Part 2: ${answer}`);
