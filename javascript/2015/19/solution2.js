/**
 * Advent of Code 2015 - Day 19: Medicine for Rudolph - Molecule Fabrication
 * https://adventofcode.com/2015/day/19
 *
 * Find the minimum number of steps to fabricate the medicine molecule
 * starting from a single electron 'e', using the available replacements.
 *
 * This solution uses a mathematical formula based on the structure of the
 * replacement rules in the AoC input.
 */

import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const INPUT_FILE = join(__dirname, '../../../aoc-data/2015/19/input');

function solvePart2() {
  const lines = readFileSync(INPUT_FILE, 'utf-8').trim().split('\n');

  let medicineMolecule = '';
  for (const line of lines) {
    if (!line.trim()) {
      continue;
    }
    if (!line.includes('=>')) {
      medicineMolecule = line.trim();
    }
  }

  // Count atoms (each uppercase letter represents one atom/element)
  const numAtoms = (medicineMolecule.match(/[A-Z]/g) || []).length;

  // Count special structural tokens
  const numRn = (medicineMolecule.match(/Rn/g) || []).length;
  const numAr = (medicineMolecule.match(/Ar/g) || []).length;
  const numY = (medicineMolecule.match(/Y/g) || []).length;

  // Apply the formula to calculate minimum fabrication steps
  const fabricationSteps = numAtoms - numRn - numAr - 2 * numY - 1;

  return fabricationSteps;
}

const answer = solvePart2();
console.log(`Part 2: ${answer}`);
