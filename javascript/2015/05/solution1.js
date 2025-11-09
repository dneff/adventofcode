/**
 * Advent of Code 2015 - Day 5: Doesn't He Have Intern-Elves For This?
 * https://adventofcode.com/2015/day/5
 *
 * Determines how many strings are "nice" based on the old rules.
 */

import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const INPUT_FILE = join(__dirname, '../../../aoc-data/2015/5/input');

function propertyOne(s) {
  // Checks if string contains at least 3 vowels
  const vowels = ['a', 'e', 'i', 'o', 'u'];
  let vowelCount = 0;

  for (const char of s) {
    if (vowels.includes(char)) {
      vowelCount++;
    }
  }

  return vowelCount >= 3;
}

function propertyTwo(s) {
  // Checks if at least one letter appears twice in a row
  for (let idx = 1; idx < s.length; idx++) {
    if (s[idx] === s[idx - 1]) {
      return true;
    }
  }
  return false;
}

function propertyThree(s) {
  // Checks if no forbidden pairs are in string
  const badPairs = ['ab', 'cd', 'pq', 'xy'];
  for (const pair of badPairs) {
    if (s.includes(pair)) {
      return false;
    }
  }
  return true;
}

function solvePart1() {
  const lines = readFileSync(INPUT_FILE, 'utf-8').trim().split('\n');
  const nice = [];

  for (const line of lines) {
    const str = line.trim();
    if (propertyOne(str) && propertyTwo(str) && propertyThree(str)) {
      nice.push(str);
    }
  }

  return nice.length;
}

const answer = solvePart1();
console.log(`Part 1: ${answer}`);
