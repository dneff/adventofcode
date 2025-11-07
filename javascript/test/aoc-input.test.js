/**
 * Tests for AoCInput class
 */

import { describe, it, expect } from '@jest/globals';
import { AoCInput } from '../aoc-helpers.js';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const fixturesPath = join(__dirname, 'fixtures');

describe('AoCInput', () => {
  describe('readLines', () => {
    it('should read all lines from a file', () => {
      const lines = AoCInput.readLines(join(fixturesPath, 'test-lines.txt'));
      expect(lines).toEqual(['line 1', 'line 2', 'line 3', '']);
    });

    it('should strip whitespace by default', () => {
      const lines = AoCInput.readLines(join(fixturesPath, 'test-spaces.txt'));
      expect(lines).toEqual(['leading spaces', 'trailing spaces', 'both', '']);
    });

    it('should preserve leading spaces when requested', () => {
      const lines = AoCInput.readLines(join(fixturesPath, 'test-spaces.txt'), true);
      expect(lines[0]).toBe('  leading spaces');
      expect(lines[1]).toBe('trailing spaces');
      expect(lines[2]).toBe('  both');
    });

    it('should throw error for non-existent file', () => {
      expect(() => {
        AoCInput.readLines('nonexistent.txt');
      }).toThrow();
    });
  });

  describe('readGrid', () => {
    it('should read file into a 2D grid object', () => {
      const grid = AoCInput.readGrid(join(fixturesPath, 'test-grid.txt'));
      expect(grid['0,0']).toBe('A');
      expect(grid['1,0']).toBe('B');
      expect(grid['2,0']).toBe('C');
      expect(grid['0,1']).toBe('D');
      expect(grid['1,1']).toBe('E');
      expect(grid['2,1']).toBe('F');
      expect(grid['0,2']).toBe('G');
      expect(grid['1,2']).toBe('H');
      expect(grid['2,2']).toBe('I');
    });

    it('should handle empty grid', () => {
      const grid = AoCInput.readGrid(join(fixturesPath, 'test-empty.txt'));
      expect(Object.keys(grid).length).toBe(0);
    });

    it('should throw error for non-existent file', () => {
      expect(() => {
        AoCInput.readGrid('nonexistent.txt');
      }).toThrow();
    });
  });

  describe('readNumbers', () => {
    it('should read all integers from file', () => {
      const numbers = AoCInput.readNumbers(join(fixturesPath, 'test-numbers.txt'));
      expect(numbers).toEqual([42, -17, 100, 0]);
    });

    it('should throw error for non-numeric data', () => {
      expect(() => {
        AoCInput.readNumbers(join(fixturesPath, 'test-lines.txt'));
      }).toThrow();
    });

    it('should throw error for non-existent file', () => {
      expect(() => {
        AoCInput.readNumbers('nonexistent.txt');
      }).toThrow();
    });
  });

  describe('readSections', () => {
    it('should split file by empty lines', () => {
      const sections = AoCInput.readSections(join(fixturesPath, 'test-sections.txt'));
      expect(sections).toEqual([
        ['section 1 line 1', 'section 1 line 2'],
        ['section 2 line 1', 'section 2 line 2', 'section 2 line 3'],
        ['section 3 line 1'],
      ]);
    });

    it('should handle single section', () => {
      const sections = AoCInput.readSections(join(fixturesPath, 'test-lines.txt'));
      expect(sections.length).toBe(1);
      expect(sections[0]).toContain('line 1');
    });

    it('should throw error for non-existent file', () => {
      expect(() => {
        AoCInput.readSections('nonexistent.txt');
      }).toThrow();
    });
  });

  describe('parseNumbers', () => {
    it('should extract all integers from a string', () => {
      const numbers = AoCInput.parseNumbers('abc 123 def -456 ghi 789');
      expect(numbers).toEqual([123, -456, 789]);
    });

    it('should handle negative numbers', () => {
      const numbers = AoCInput.parseNumbers('Temperature: -15 degrees');
      expect(numbers).toEqual([-15]);
    });

    it('should handle multiple numbers on one line', () => {
      const numbers = AoCInput.parseNumbers('1,2,3,4,5');
      expect(numbers).toEqual([1, 2, 3, 4, 5]);
    });

    it('should return empty array for no numbers', () => {
      const numbers = AoCInput.parseNumbers('no numbers here');
      expect(numbers).toEqual([]);
    });

    it('should handle zero', () => {
      const numbers = AoCInput.parseNumbers('value: 0');
      expect(numbers).toEqual([0]);
    });
  });
});
