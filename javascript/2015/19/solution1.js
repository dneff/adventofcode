/**
 * Advent of Code 2015 - Day 19: Medicine for Rudolph
 * https://adventofcode.com/2015/day/19
 *
 * Count how many distinct molecules can be created by doing exactly one
 * replacement on the starting medicine molecule.
 */

import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const INPUT_FILE = join(__dirname, '../../../aoc-data/2015/19/input');

function solvePart1() {
  const lines = readFileSync(INPUT_FILE, 'utf-8').trim().split('\n');

  const replacements = {};

  let medicineMolecule = '';

  for (const line of lines) {
    if (!line.trim()) {
      continue;
    }
    if (line.includes('=>')) {
      const [sourcePattern, replacementPattern] = line.trim().split(' => ');
      if (!replacements[sourcePattern]) {
        replacements[sourcePattern] = [];
      }
      replacements[sourcePattern].push(replacementPattern);
    } else {
      medicineMolecule = line.trim();
    }
  }

  const distinctMolecules = new Set();

  for (const sourcePattern of Object.keys(replacements)) {
    const regex = new RegExp(sourcePattern, 'g');
    let match;
    const matches = [];

    while ((match = regex.exec(medicineMolecule)) !== null) {
      matches.push({ start: match.index, end: match.index + sourcePattern.length });
      regex.lastIndex = match.index + 1;
    }

    for (const { start, end } of matches) {
      for (const replacementPattern of replacements[sourcePattern]) {
        const newMolecule =
          medicineMolecule.slice(0, start) + replacementPattern + medicineMolecule.slice(end);
        distinctMolecules.add(newMolecule);
      }
    }
  }

  return distinctMolecules.size;
}

const answer = solvePart1();
console.log(`Part 1: ${answer}`);
