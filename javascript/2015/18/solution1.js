/**
 * Advent of Code 2015 - Day 18: Like a GIF For Your Yard
 * https://adventofcode.com/2015/day/18
 *
 * Simulates a grid of lights following Conway's Game of Life rules.
 */

import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const INPUT_FILE = join(__dirname, '../../../aoc-data/2015/18/input');

class Display {
  constructor() {
    this.lights = new Map();
    this.step = 0;
    this.width = 0;
  }

  add(light) {
    const key = `${light[0]},${light[1]}`;
    this.lights.set(key, true);
  }

  getNeighbors(point) {
    const neighbors = [];
    const offsets = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]];

    for (const offset of offsets) {
      const possible = [point[0] + offset[0], point[1] + offset[1]];
      if (Math.max(...possible) > this.width || Math.min(...possible) < 0) {
        continue;
      }
      neighbors.push(possible);
    }
    return neighbors;
  }

  cycle() {
    const neighbors = new Map();

    for (const [key, _] of this.lights) {
      const [r, c] = key.split(',').map(Number);
      for (const neighbor of this.getNeighbors([r, c])) {
        const neighborKey = `${neighbor[0]},${neighbor[1]}`;
        neighbors.set(neighborKey, (neighbors.get(neighborKey) || 0) + 1);
      }
    }

    const off = [];
    for (const [key, _] of this.lights) {
      const count = neighbors.get(key) || 0;
      if (count !== 2 && count !== 3) {
        off.push(key);
      }
    }

    const on = [];
    for (const [key, count] of neighbors) {
      if (count === 3) {
        on.push(key);
      }
    }

    for (const light of off) {
      this.lights.delete(light);
    }
    for (const light of on) {
      this.lights.set(light, true);
    }

    this.step += 1;
  }
}

function solvePart1() {
  const lines = readFileSync(INPUT_FILE, 'utf-8').trim().split('\n');

  const stepCount = 100;
  const xmasLights = new Display();

  let width = 0;
  for (let row = 0; row < lines.length; row++) {
    const line = lines[row].trim();
    for (let column = 0; column < line.length; column++) {
      if (line[column] === '#') {
        xmasLights.add([row, column]);
      }
    }
    width = Math.max(width, row);
  }

  xmasLights.width = width;

  while (xmasLights.step < stepCount) {
    xmasLights.cycle();
  }

  return xmasLights.lights.size;
}

const answer = solvePart1();
console.log(`Part 1: ${answer}`);
