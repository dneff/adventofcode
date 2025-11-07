/**
 * Tests for AoCUtils class
 */

import { describe, it, expect, jest } from '@jest/globals';
import { AoCUtils } from '../aoc-helpers.js';

describe('AoCUtils', () => {
  describe('printSolution', () => {
    it('should print solution in correct format', () => {
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation();

      AoCUtils.printSolution(1, 42);
      expect(consoleSpy).toHaveBeenCalledWith('Part 1: 42');

      AoCUtils.printSolution(2, 'answer');
      expect(consoleSpy).toHaveBeenCalledWith('Part 2: answer');

      consoleSpy.mockRestore();
    });
  });

  describe('chunks', () => {
    it('should split array into chunks', () => {
      const arr = [1, 2, 3, 4, 5, 6, 7, 8, 9];
      expect(AoCUtils.chunks(arr, 3)).toEqual([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
      ]);
    });

    it('should handle partial last chunk', () => {
      const arr = [1, 2, 3, 4, 5, 6, 7];
      expect(AoCUtils.chunks(arr, 3)).toEqual([[1, 2, 3], [4, 5, 6], [7]]);
    });

    it('should handle chunk size larger than array', () => {
      const arr = [1, 2, 3];
      expect(AoCUtils.chunks(arr, 10)).toEqual([[1, 2, 3]]);
    });

    it('should handle empty array', () => {
      expect(AoCUtils.chunks([], 3)).toEqual([]);
    });

    it('should handle chunk size of 1', () => {
      const arr = [1, 2, 3];
      expect(AoCUtils.chunks(arr, 1)).toEqual([[1], [2], [3]]);
    });

    it('should work with strings', () => {
      const arr = ['a', 'b', 'c', 'd', 'e'];
      expect(AoCUtils.chunks(arr, 2)).toEqual([['a', 'b'], ['c', 'd'], ['e']]);
    });
  });

  describe('binaryToDecimal', () => {
    it('should convert binary string to decimal', () => {
      expect(AoCUtils.binaryToDecimal('1010')).toBe(10);
      expect(AoCUtils.binaryToDecimal('1111')).toBe(15);
      expect(AoCUtils.binaryToDecimal('10000')).toBe(16);
    });

    it('should handle zero', () => {
      expect(AoCUtils.binaryToDecimal('0')).toBe(0);
      expect(AoCUtils.binaryToDecimal('0000')).toBe(0);
    });

    it('should handle single bits', () => {
      expect(AoCUtils.binaryToDecimal('1')).toBe(1);
    });

    it('should handle large numbers', () => {
      expect(AoCUtils.binaryToDecimal('11111111')).toBe(255);
      expect(AoCUtils.binaryToDecimal('100000000')).toBe(256);
    });
  });

  describe('charToPriority', () => {
    it('should convert lowercase letters to 1-26', () => {
      expect(AoCUtils.charToPriority('a')).toBe(1);
      expect(AoCUtils.charToPriority('b')).toBe(2);
      expect(AoCUtils.charToPriority('z')).toBe(26);
    });

    it('should convert uppercase letters to 27-52', () => {
      expect(AoCUtils.charToPriority('A')).toBe(27);
      expect(AoCUtils.charToPriority('B')).toBe(28);
      expect(AoCUtils.charToPriority('Z')).toBe(52);
    });

    it('should handle middle letters correctly', () => {
      expect(AoCUtils.charToPriority('m')).toBe(13);
      expect(AoCUtils.charToPriority('M')).toBe(39);
    });

    it('should return 0 for non-letter characters', () => {
      expect(AoCUtils.charToPriority('1')).toBe(0);
      expect(AoCUtils.charToPriority(' ')).toBe(0);
      expect(AoCUtils.charToPriority('!')).toBe(0);
    });
  });
});
