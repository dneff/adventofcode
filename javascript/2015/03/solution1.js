/**
 * Advent of Code 2015 - Day 3: Perfectly Spherical Houses in a Vacuum
 * https://adventofcode.com/2015/day/3
 *
 * Counts how many houses receive at least one present.
 */

import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const INPUT_FILE = join(__dirname, '../../../aoc-data/2015/3/input');

function solvePart1() {
  const path = readFileSync(INPUT_FILE, 'utf-8').trim();

  const move = {
    '^': [0, 1],
    '>': [1, 0],
    'v': [0, -1],
    '<': [-1, 0],
  };

  const houses = new Map();
  let location = [0, 0];
  houses.set(location.join(','), 1);

  for (const direction of path) {
    const [dx, dy] = move[direction];
    location = [location[0] + dx, location[1] + dy];
    const key = location.join(',');
    houses.set(key, (houses.get(key) || 0) + 1);
  }

  return houses.size;
}

const answer = solvePart1();
console.log(`Part 1: ${answer}`);
