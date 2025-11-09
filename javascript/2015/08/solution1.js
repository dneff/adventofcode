/**
 * Advent of Code 2015 - Day 8: Matchsticks
 * https://adventofcode.com/2015/day/8
 *
 * Calculates the difference between code representation and in-memory string length.
 */

import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const INPUT_FILE = join(__dirname, '../../../aoc-data/2015/8/input');

function solvePart1() {
  const lines = readFileSync(INPUT_FILE, 'utf-8').trim().split('\n');
  let diff = 0;

  for (const line of lines) {
    const trimmed = line.trim();
    // Remove outer quotes and process escape sequences
    let processed = trimmed.slice(1, -1);

    // Replace escape sequences
    processed = processed.replace(/\\x[0-9a-f]{2}/g, 'X'); // \xNN -> single char
    processed = processed.replace(/\\\\/g, '\\'); // \\ -> \
    processed = processed.replace(/\\"/g, '"'); // \" -> "

    diff += trimmed.length - processed.length;
  }

  return diff;
}

const answer = solvePart1();
console.log(`Part 1: ${answer}`);
