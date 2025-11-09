/**
 * Advent of Code 2015 - Day 6: Probably a Fire Hazard
 * https://adventofcode.com/2015/day/6
 *
 * Controls a grid of lights with on, off, and toggle commands.
 */

import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const INPUT_FILE = join(__dirname, '../../../aoc-data/2015/6/input');

class Lights {
  constructor() {
    this.grid = new Map();
  }

  on(start, end) {
    for (let row = start[0]; row <= end[0]; row++) {
      for (let col = start[1]; col <= end[1]; col++) {
        this.grid.set(`${row},${col}`, 1);
      }
    }
  }

  off(start, end) {
    for (let row = start[0]; row <= end[0]; row++) {
      for (let col = start[1]; col <= end[1]; col++) {
        this.grid.set(`${row},${col}`, 0);
      }
    }
  }

  toggle(start, end) {
    for (let row = start[0]; row <= end[0]; row++) {
      for (let col = start[1]; col <= end[1]; col++) {
        const key = `${row},${col}`;
        const current = this.grid.get(key) || 0;
        this.grid.set(key, (current + 1) % 2);
      }
    }
  }

  lit() {
    let count = 0;
    for (const value of this.grid.values()) {
      count += value;
    }
    return count;
  }
}

function solvePart1() {
  const lines = readFileSync(INPUT_FILE, 'utf-8').trim().split('\n');
  const display = new Lights();

  for (const line of lines) {
    const processed = line
      .trim()
      .replace('turn on', 'on')
      .replace('turn off', 'off')
      .replace('through', '');

    const parts = processed.split(/\s+/);
    const action = parts[0];
    const start = parts[1].split(',').map(Number);
    const end = parts[2].split(',').map(Number);

    display[action](start, end);
  }

  return display.lit();
}

const answer = solvePart1();
console.log(`Part 1: ${answer}`);
