/**
 * Advent of Code 2015 - Day 12: JSAbacusFramework.io
 * https://adventofcode.com/2015/day/12
 *
 * Sums all numbers in a JSON document, ignoring objects with "red" values.
 */

import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const INPUT_FILE = join(__dirname, '../../../aoc-data/2015/12/input');

function getValue(data) {
  let result = 0;

  if (typeof data === 'string' || typeof data === 'number') {
    if (typeof data === 'number') {
      return data;
    }
    try {
      return parseInt(data, 10);
    } catch (e) {
      return 0;
    }
  } else if (Array.isArray(data)) {
    for (const d of data) {
      result += getValue(d);
    }
  } else if (typeof data === 'object' && data !== null) {
    const values = Object.values(data);
    if (!values.includes('red')) {
      for (const d of values) {
        result += getValue(d);
      }
    }
  }

  return result;
}

function solvePart2() {
  const jsonData = readFileSync(INPUT_FILE, 'utf-8').trim();
  const data = JSON.parse(jsonData);

  return getValue(data);
}

const answer = solvePart2();
console.log(`Part 2: ${answer}`);
