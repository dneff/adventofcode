/**
 * Advent of Code 2015 - Day 20: Infinite Elves and Infinite Houses
 * https://adventofcode.com/2015/day/20
 *
 * Find the lowest house number that receives at least the target number of presents.
 */

import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const INPUT_FILE = join(__dirname, '../../../aoc-data/2015/20/input');

function solvePart1() {
  const targetPresents = parseInt(readFileSync(INPUT_FILE, 'utf-8').trim(), 10);

  // Upper bound estimate
  const maxHouse = Math.floor(targetPresents / 30);

  // Initialize presents array
  const presents = new Array(maxHouse + 1).fill(0);

  // Track the minimum house number that could still win
  let minPossibleAnswer = maxHouse;

  // Sieve approach: each elf delivers to all their houses
  for (let elfNumber = 1; elfNumber <= maxHouse; elfNumber++) {
    // Early exit
    if (elfNumber > minPossibleAnswer) {
      break;
    }

    const presentsToDeliver = 10 * elfNumber;

    // Deliver to all houses that are multiples of elfNumber
    for (let house = elfNumber; house <= minPossibleAnswer; house += elfNumber) {
      presents[house] += presentsToDeliver;

      // Check if this house just reached the target
      if (presents[house] >= targetPresents && house < minPossibleAnswer) {
        minPossibleAnswer = house;
      }
    }
  }

  return minPossibleAnswer < maxHouse ? minPossibleAnswer : null;
}

const answer = solvePart1();
console.log(`Part 1: ${answer}`);
