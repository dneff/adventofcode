/**
 * Advent of Code 2015 - Day 16: Aunt Sue
 * https://adventofcode.com/2015/day/16
 *
 * Finds which Aunt Sue sent you a gift with the updated reading rules.
 */

import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const INPUT_FILE = join(__dirname, '../../../aoc-data/2015/16/input');

function scoreAunt(details) {
  const detected = {
    children: 3,
    cats: 7,
    samoyeds: 2,
    pomeranians: 3,
    akitas: 0,
    vizslas: 0,
    goldfish: 5,
    trees: 3,
    cars: 2,
    perfumes: 1,
  };

  let result = 0;

  for (const [k, v] of Object.entries(details)) {
    if (['cats', 'trees'].includes(k)) {
      if (detected[k] < v) {
        result += 1;
      }
    } else if (['pomeranians', 'goldfish'].includes(k)) {
      if (detected[k] > v) {
        result += 1;
      }
    } else {
      if (detected[k] === v) {
        result += 1;
      }
    }
  }

  return result;
}

function solvePart2() {
  const lines = readFileSync(INPUT_FILE, 'utf-8').trim().split('\n');

  const aunts = {};
  const matches = {};

  for (const line of lines) {
    let cleaned = line.trim().replace('Sue ', '');
    cleaned = cleaned.replace(/:/g, '').replace(/,/g, '');
    const parts = cleaned.split(' ');

    const aunt = parseInt(parts.shift(), 10);
    aunts[aunt] = {};

    while (parts.length > 0) {
      const k = parts.shift();
      const v = parseInt(parts.shift(), 10);
      aunts[aunt][k] = v;
    }
  }

  for (const [aunt, details] of Object.entries(aunts)) {
    matches[aunt] = scoreAunt(details);
  }

  const maxAunt = Object.entries(matches).reduce((a, b) => (b[1] > a[1] ? b : a))[0];
  return parseInt(maxAunt, 10);
}

const answer = solvePart2();
console.log(`Part 2: ${answer}`);
