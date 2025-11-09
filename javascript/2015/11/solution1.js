/**
 * Advent of Code 2015 - Day 11: Corporate Policy
 * https://adventofcode.com/2015/day/11
 *
 * Finds the next valid password after Santa's current password.
 */

import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const INPUT_FILE = join(__dirname, '../../../aoc-data/2015/11/input');

class PasswordManager {
  constructor() {
    this.password = '';
  }

  add(pwd) {
    this.password = pwd;
  }

  hasPair(s) {
    for (let i = 0; i < s.length - 1; i++) {
      if (s[i] === s[i + 1]) {
        return true;
      }
    }
    return false;
  }

  verify(s) {
    // must not contain i, o, l
    const invalid = ['i', 'o', 'l'];
    for (const char of invalid) {
      if (s.includes(char)) {
        return false;
      }
    }

    // must contain two non-overlapping pairs
    let pairs = false;
    for (let i = 0; i < s.length - 1; i++) {
      if (s[i] === s[i + 1]) {
        if (this.hasPair(s.slice(i + 2))) {
          pairs = true;
          break;
        }
      }
    }
    if (!pairs) {
      return false;
    }

    // must contain straight of at least three letters
    let triplets = false;
    const alphabet = 'abcdefghijklmnopqrstuvwxyz';
    for (let i = 0; i < s.length - 2; i++) {
      const letter = s[i];
      const letterPos = alphabet.indexOf(letter);
      const testTriplet = alphabet.slice(letterPos, letterPos + 3);
      if (testTriplet.length !== 3) {
        continue;
      }
      if (s.includes(testTriplet)) {
        triplets = true;
        break;
      }
    }

    return triplets;
  }

  increment(s) {
    const alphabet = 'abcdefghijklmnopqrstuvwxyz';
    const iterator = s.split('').map(c => alphabet.indexOf(c));
    iterator[iterator.length - 1] += 1;

    for (let i = iterator.length - 1; i > 0; i--) {
      iterator[i - 1] += Math.floor(iterator[i] / alphabet.length);
      iterator[i] %= alphabet.length;
    }
    iterator[0] %= alphabet.length;

    return iterator.map(i => alphabet[i]).join('');
  }

  next() {
    let possible = this.increment(this.password);
    while (!this.verify(possible)) {
      possible = this.increment(possible);
    }
    this.password = possible;
  }
}

function solvePart1() {
  const input = readFileSync(INPUT_FILE, 'utf-8').trim();

  const pm = new PasswordManager();
  pm.add(input);
  pm.next();

  return pm.password;
}

const answer = solvePart1();
console.log(`Part 1: ${answer}`);
