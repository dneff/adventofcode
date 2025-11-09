/**
 * Advent of Code 2015 - Day 20: Infinite Elves and Infinite Houses
 * https://adventofcode.com/2015/day/20
 *
 * Find the lowest house number with modified elf delivery rules.
 */

import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const INPUT_FILE = join(__dirname, '../../../aoc-data/2015/20/input');

function solvePart2() {
  const targetPresents = parseInt(readFileSync(INPUT_FILE, 'utf-8').trim(), 10);

  // Upper bound estimate
  const maxHouse = Math.floor(targetPresents / 11);

  // Initialize presents array
  const presents = new Array(maxHouse + 1).fill(0);

  // Track the minimum house number that has reached the target
  let minPossibleAnswer = maxHouse;

  // Sieve approach: each elf delivers to their houses
  for (let elfNumber = 1; elfNumber <= maxHouse; elfNumber++) {
    // Early exit
    if (elfNumber > minPossibleAnswer) {
      break;
    }

    const presentsToDeliver = 11 * elfNumber;
    const maxHousesPerElf = 50;

    // Calculate the last house this elf will visit
    const lastHouseVisited = Math.min(elfNumber * maxHousesPerElf, minPossibleAnswer);

    // Deliver presents to each house this elf visits
    for (let house = elfNumber; house <= lastHouseVisited; house += elfNumber) {
      presents[house] += presentsToDeliver;

      // Check if this house just reached the target
      if (presents[house] >= targetPresents && house < minPossibleAnswer) {
        minPossibleAnswer = house;
      }
    }
  }

  return minPossibleAnswer < maxHouse ? minPossibleAnswer : null;
}

const answer = solvePart2();
console.log(`Part 2: ${answer}`);
