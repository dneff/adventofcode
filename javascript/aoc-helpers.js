/**
 * Advent of Code Helper Classes
 *
 * A comprehensive collection of utilities commonly used across AoC solutions.
 * JavaScript implementation matching Python helper library functionality.
 */

import { readFileSync } from 'fs';

/**
 * Input reading and parsing utilities.
 */
class AoCInput {
  /**
   * Read all lines from file, stripped of whitespace.
   *
   * @param {string} filename - Path to the file to read
   * @param {boolean} [preserveLeadingSpace=false] - If true, only strip trailing whitespace.
   *                                                  If false (default), strip all whitespace.
   * @returns {string[]} List of lines from the file
   * @throws {Error} If file cannot be read
   */
  static readLines(filename, preserveLeadingSpace = false) {
    try {
      const content = readFileSync(filename, 'utf-8');
      const lines = content.split('\n');

      if (preserveLeadingSpace) {
        // Only strip trailing newline and carriage return
        return lines.map((line) => line.replace(/\r?\n?$/, ''));
      } else {
        // Strip all whitespace from both ends
        return lines.map((line) => line.trim());
      }
    } catch (error) {
      throw new Error(`Failed to read file ${filename}: ${error.message}`);
    }
  }

  /**
   * Read file into a 2D grid object with "x,y" string keys mapping to characters.
   *
   * @param {string} filename - Path to the file to read
   * @returns {Object.<string, string>} Grid object with "x,y" keys mapping to character values
   * @throws {Error} If file cannot be read
   */
  static readGrid(filename) {
    try {
      const content = readFileSync(filename, 'utf-8');
      const lines = content.split('\n').map((line) => line.trimEnd());
      const grid = {};

      for (let y = 0; y < lines.length; y++) {
        const line = lines[y];
        for (let x = 0; x < line.length; x++) {
          grid[`${x},${y}`] = line[x];
        }
      }

      return grid;
    } catch (error) {
      throw new Error(`Failed to read grid from ${filename}: ${error.message}`);
    }
  }

  /**
   * Read all integers from file (one per line).
   *
   * @param {string} filename - Path to the file to read
   * @returns {number[]} Array of integers
   * @throws {Error} If file cannot be read or contains non-numeric data
   */
  static readNumbers(filename) {
    try {
      const lines = this.readLines(filename);
      return lines
        .filter((line) => line.length > 0)
        .map((line) => {
          const num = parseInt(line, 10);
          if (isNaN(num)) {
            throw new Error(`Invalid number: ${line}`);
          }
          return num;
        });
    } catch (error) {
      throw new Error(`Failed to read numbers from ${filename}: ${error.message}`);
    }
  }

  /**
   * Read file split by empty lines into sections.
   *
   * @param {string} filename - Path to the file to read
   * @returns {string[][]} Array of sections, each containing an array of lines
   * @throws {Error} If file cannot be read
   */
  static readSections(filename) {
    try {
      const content = readFileSync(filename, 'utf-8').trim();
      return content.split('\n\n').map((section) => section.split('\n'));
    } catch (error) {
      throw new Error(`Failed to read sections from ${filename}: ${error.message}`);
    }
  }

  /**
   * Extract all integers (including negative) from a string.
   *
   * @param {string} text - Text to parse
   * @returns {number[]} Array of integers found in the text
   */
  static parseNumbers(text) {
    const matches = text.match(/-?\d+/g);
    return matches ? matches.map((n) => parseInt(n, 10)) : [];
  }
}

/**
 * Mathematical utilities.
 */
class MathUtils {
  /**
   * Calculate GCD (Greatest Common Divisor) of two numbers using Euclidean algorithm.
   *
   * @param {number} a - First number
   * @param {number} b - Second number
   * @returns {number} GCD of a and b
   */
  static gcd(a, b) {
    a = Math.abs(a);
    b = Math.abs(b);
    while (b !== 0) {
      const temp = b;
      b = a % b;
      a = temp;
    }
    return a;
  }

  /**
   * Calculate GCD of multiple numbers.
   *
   * @param {...number} args - Numbers to find GCD of
   * @returns {number} GCD of all numbers
   * @throws {Error} If no arguments provided
   */
  static gcdMultiple(...args) {
    if (args.length === 0) {
      throw new Error('At least one number required');
    }
    return args.reduce((acc, val) => this.gcd(acc, val));
  }

  /**
   * Calculate LCM (Least Common Multiple) of two numbers.
   *
   * @param {number} a - First number
   * @param {number} b - Second number
   * @returns {number} LCM of a and b
   */
  static lcm(a, b) {
    return Math.abs(a * b) / this.gcd(a, b);
  }

  /**
   * Calculate LCM of multiple numbers.
   *
   * @param {...number} args - Numbers to find LCM of
   * @returns {number} LCM of all numbers
   * @throws {Error} If no arguments provided
   */
  static lcmMultiple(...args) {
    if (args.length === 0) {
      throw new Error('At least one number required');
    }
    return args.reduce((acc, val) => this.lcm(acc, val));
  }

  /**
   * Calculate Manhattan distance between two points.
   *
   * @param {[number, number]} p1 - First point as [x, y]
   * @param {[number, number]} p2 - Second point as [x, y]
   * @returns {number} Manhattan distance
   */
  static manhattanDistance(p1, p2) {
    return Math.abs(p1[0] - p2[0]) + Math.abs(p1[1] - p2[1]);
  }

  /**
   * Return the sign of a number.
   *
   * @param {number} x - Number to get sign of
   * @returns {number} -1 for negative, 0 for zero, 1 for positive
   */
  static sign(x) {
    return x > 0 ? 1 : x < 0 ? -1 : 0;
  }
}

/**
 * General utility functions.
 */
class AoCUtils {
  /**
   * Standard solution printing format.
   *
   * @param {number} part - Part number (1 or 2)
   * @param {*} answer - The answer to print
   */
  static printSolution(part, answer) {
    console.log(`Part ${part}: ${answer}`);
  }

  /**
   * Split array into chunks of size n.
   *
   * @param {Array} lst - Array to chunk
   * @param {number} n - Chunk size
   * @returns {Array[]} Array of chunks
   */
  static chunks(lst, n) {
    const result = [];
    for (let i = 0; i < lst.length; i += n) {
      result.push(lst.slice(i, i + n));
    }
    return result;
  }

  /**
   * Convert binary string to decimal number.
   *
   * @param {string} binaryStr - Binary string (e.g., "1010")
   * @returns {number} Decimal number
   */
  static binaryToDecimal(binaryStr) {
    return parseInt(binaryStr, 2);
  }

  /**
   * Convert character to priority value.
   * Lowercase a-z: 1-26
   * Uppercase A-Z: 27-52
   *
   * @param {string} char - Single character
   * @returns {number} Priority value (0 if not a letter)
   */
  static charToPriority(char) {
    const code = char.charCodeAt(0);
    const aLower = 'a'.charCodeAt(0);
    const zLower = 'z'.charCodeAt(0);
    const aUpper = 'A'.charCodeAt(0);
    const zUpper = 'Z'.charCodeAt(0);

    if (code >= aLower && code <= zLower) {
      return code - aLower + 1;
    } else if (code >= aUpper && code <= zUpper) {
      return code - aUpper + 27;
    }
    return 0;
  }
}

export { AoCInput, MathUtils, AoCUtils };
