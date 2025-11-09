/**
 * Advent of Code 2015 - Day 23: Opening the Turing Lock
 * https://adventofcode.com/2015/day/23
 *
 * Simulates a simple computer with a small instruction set.
 */

import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const INPUT_FILE = join(__dirname, '../../../aoc-data/2015/23/input');

class Computer {
  constructor() {
    this.index = 0;
    this.registers = { a: 0, b: 0 };
    this.instructions = [];
  }

  load(data) {
    for (const line of data) {
      this.instructions.push(line.trim().split(' '));
    }
  }

  run() {
    while (this.index < this.instructions.length) {
      const inst = this.instructions[this.index];
      const command = this[inst[0]].bind(this);
      if (inst.length === 2) {
        command(inst[inst.length - 1]);
      } else {
        command(inst[1][0], inst[inst.length - 1]);
      }
    }
  }

  hlf(r) {
    this.registers[r] = Math.floor(this.registers[r] / 2);
    this.index += 1;
  }

  tpl(r) {
    this.registers[r] *= 3;
    this.index += 1;
  }

  inc(r) {
    this.registers[r] += 1;
    this.index += 1;
  }

  jmp(offset) {
    this.index += parseInt(offset, 10);
  }

  jie(r, offset) {
    if (this.registers[r] % 2 === 0) {
      this.index += parseInt(offset, 10);
    } else {
      this.index += 1;
    }
  }

  jio(r, offset) {
    if (this.registers[r] === 1) {
      this.index += parseInt(offset, 10);
    } else {
      this.index += 1;
    }
  }
}

function solvePart1() {
  const lines = readFileSync(INPUT_FILE, 'utf-8').trim().split('\n');
  const gift = new Computer();
  gift.load(lines);
  gift.run();
  return gift.registers['b'];
}

const answer = solvePart1();
console.log(`Part 1: ${answer}`);
