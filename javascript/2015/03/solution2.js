/**
 * Advent of Code 2015 - Day 3, Part 2
 * https://adventofcode.com/2015/day/3
 *
 * Counts how many houses receive at least one present from Santa and Robo-Santa.
 */

import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const INPUT_FILE = join(__dirname, '../../../aoc-data/2015/3/input');

function solvePart2() {
  const path = readFileSync(INPUT_FILE, 'utf-8').trim();

  const move = {
    '^': [0, 1],
    '>': [1, 0],
    'v': [0, -1],
    '<': [-1, 0],
  };

  const houses = new Map();
  const locations = [
    [0, 0], // Santa
    [0, 0], // Robo-Santa
  ];

  // Mark starting location
  for (const loc of locations) {
    const key = loc.join(',');
    houses.set(key, (houses.get(key) || 0) + 1);
  }

  for (let idx = 0; idx < path.length; idx++) {
    const turn = idx % 2;
    const direction = path[idx];
    const [dx, dy] = move[direction];

    locations[turn] = [locations[turn][0] + dx, locations[turn][1] + dy];
    const key = locations[turn].join(',');
    houses.set(key, (houses.get(key) || 0) + 1);
  }

  return houses.size;
}

const answer = solvePart2();
console.log(`Part 2: ${answer}`);
