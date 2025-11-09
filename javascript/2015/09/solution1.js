/**
 * Advent of Code 2015 - Day 9: All in a Single Night
 * https://adventofcode.com/2015/day/9
 *
 * Finds the shortest route visiting all cities.
 */

import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const INPUT_FILE = join(__dirname, '../../../aoc-data/2015/9/input');

function* permutations(arr) {
  if (arr.length <= 1) {
    yield arr;
    return;
  }

  for (let i = 0; i < arr.length; i++) {
    const rest = [...arr.slice(0, i), ...arr.slice(i + 1)];
    for (const perm of permutations(rest)) {
      yield [arr[i], ...perm];
    }
  }
}

function solvePart1() {
  const lines = readFileSync(INPUT_FILE, 'utf-8').trim().split('\n');
  const cities = {};

  for (const line of lines) {
    const [c1c2, distanceStr] = line.trim().split(' = ');
    const [c1, c2] = c1c2.split(' to ');
    const distance = parseInt(distanceStr, 10);

    if (!(c1 in cities)) {
      cities[c1] = {};
    }
    if (!(c2 in cities)) {
      cities[c2] = {};
    }

    cities[c1][c2] = distance;
    cities[c2][c1] = distance;
  }

  const cityNames = Object.keys(cities);
  let shortest = Infinity;

  for (const perm of permutations(cityNames)) {
    let routeDistance = 0;
    for (let i = 0; i < perm.length - 1; i++) {
      routeDistance += cities[perm[i]][perm[i + 1]];
    }
    shortest = Math.min(shortest, routeDistance);
  }

  return shortest;
}

const answer = solvePart1();
console.log(`Part 1: ${answer}`);
