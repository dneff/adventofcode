/**
 * Advent of Code 2015 - Day 10, Part 2
 * https://adventofcode.com/2015/day/10
 *
 * Applies the Look-and-Say sequence 50 times.
 */

import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const INPUT_FILE = join(__dirname, '../../../aoc-data/2015/10/input');

class LookSay {
  constructor(start) {
    if (start.length === 0) {
      throw new Error('starting value should be at least one digit');
    }
    this.sequence = start;
  }

  step() {
    let updated = '';
    let counter = 1;

    if (this.sequence.length === 1) {
      updated = counter.toString() + this.sequence;
    } else {
      for (let idx = 1; idx < this.sequence.length; idx++) {
        const digit = this.sequence[idx];
        if (digit === this.sequence[idx - 1]) {
          counter++;
        } else {
          updated += counter.toString() + this.sequence[idx - 1];
          counter = 1;
        }
      }
      updated += counter.toString() + this.sequence[this.sequence.length - 1];
    }

    this.sequence = updated;
  }
}

function solvePart2() {
  const input = readFileSync(INPUT_FILE, 'utf-8').trim();
  const turns = 50;

  const game = new LookSay(input);
  for (let i = 0; i < turns; i++) {
    game.step();
  }

  return game.sequence.length;
}

const answer = solvePart2();
console.log(`Part 2: ${answer}`);
