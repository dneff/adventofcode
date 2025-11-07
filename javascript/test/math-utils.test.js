/**
 * Tests for MathUtils class
 */

import { describe, it, expect } from '@jest/globals';
import { MathUtils } from '../aoc-helpers.js';

describe('MathUtils', () => {
  describe('gcd', () => {
    it('should calculate GCD of two numbers', () => {
      expect(MathUtils.gcd(12, 8)).toBe(4);
      expect(MathUtils.gcd(48, 18)).toBe(6);
      expect(MathUtils.gcd(17, 13)).toBe(1);
    });

    it('should handle zero', () => {
      expect(MathUtils.gcd(0, 5)).toBe(5);
      expect(MathUtils.gcd(5, 0)).toBe(5);
      expect(MathUtils.gcd(0, 0)).toBe(0);
    });

    it('should handle negative numbers', () => {
      expect(MathUtils.gcd(-12, 8)).toBe(4);
      expect(MathUtils.gcd(12, -8)).toBe(4);
      expect(MathUtils.gcd(-12, -8)).toBe(4);
    });

    it('should handle same numbers', () => {
      expect(MathUtils.gcd(7, 7)).toBe(7);
    });
  });

  describe('gcdMultiple', () => {
    it('should calculate GCD of multiple numbers', () => {
      expect(MathUtils.gcdMultiple(12, 8, 4)).toBe(4);
      expect(MathUtils.gcdMultiple(48, 18, 24)).toBe(6);
      expect(MathUtils.gcdMultiple(10, 15, 20, 25)).toBe(5);
    });

    it('should handle single number', () => {
      expect(MathUtils.gcdMultiple(42)).toBe(42);
    });

    it('should handle two numbers', () => {
      expect(MathUtils.gcdMultiple(12, 8)).toBe(4);
    });

    it('should throw error for no arguments', () => {
      expect(() => {
        MathUtils.gcdMultiple();
      }).toThrow();
    });
  });

  describe('lcm', () => {
    it('should calculate LCM of two numbers', () => {
      expect(MathUtils.lcm(4, 6)).toBe(12);
      expect(MathUtils.lcm(3, 5)).toBe(15);
      expect(MathUtils.lcm(12, 8)).toBe(24);
    });

    it('should handle one being multiple of other', () => {
      expect(MathUtils.lcm(3, 9)).toBe(9);
      expect(MathUtils.lcm(5, 10)).toBe(10);
    });

    it('should handle same numbers', () => {
      expect(MathUtils.lcm(7, 7)).toBe(7);
    });

    it('should handle negative numbers', () => {
      expect(MathUtils.lcm(-4, 6)).toBe(12);
      expect(MathUtils.lcm(4, -6)).toBe(12);
      expect(MathUtils.lcm(-4, -6)).toBe(12);
    });
  });

  describe('lcmMultiple', () => {
    it('should calculate LCM of multiple numbers', () => {
      expect(MathUtils.lcmMultiple(4, 6, 8)).toBe(24);
      expect(MathUtils.lcmMultiple(3, 5, 7)).toBe(105);
      expect(MathUtils.lcmMultiple(2, 3, 4, 5)).toBe(60);
    });

    it('should handle single number', () => {
      expect(MathUtils.lcmMultiple(42)).toBe(42);
    });

    it('should handle two numbers', () => {
      expect(MathUtils.lcmMultiple(4, 6)).toBe(12);
    });

    it('should throw error for no arguments', () => {
      expect(() => {
        MathUtils.lcmMultiple();
      }).toThrow();
    });
  });

  describe('manhattanDistance', () => {
    it('should calculate Manhattan distance', () => {
      expect(MathUtils.manhattanDistance([0, 0], [3, 4])).toBe(7);
      expect(MathUtils.manhattanDistance([1, 1], [4, 5])).toBe(7);
      expect(MathUtils.manhattanDistance([0, 0], [0, 0])).toBe(0);
    });

    it('should handle negative coordinates', () => {
      expect(MathUtils.manhattanDistance([-1, -1], [1, 1])).toBe(4);
      expect(MathUtils.manhattanDistance([5, 3], [-2, -4])).toBe(14);
    });

    it('should be symmetric', () => {
      const p1 = [3, 7];
      const p2 = [10, 2];
      expect(MathUtils.manhattanDistance(p1, p2)).toBe(MathUtils.manhattanDistance(p2, p1));
    });
  });

  describe('sign', () => {
    it('should return 1 for positive numbers', () => {
      expect(MathUtils.sign(5)).toBe(1);
      expect(MathUtils.sign(0.1)).toBe(1);
      expect(MathUtils.sign(1000000)).toBe(1);
    });

    it('should return -1 for negative numbers', () => {
      expect(MathUtils.sign(-5)).toBe(-1);
      expect(MathUtils.sign(-0.1)).toBe(-1);
      expect(MathUtils.sign(-1000000)).toBe(-1);
    });

    it('should return 0 for zero', () => {
      expect(MathUtils.sign(0)).toBe(0);
      expect(MathUtils.sign(-0)).toBe(0);
    });
  });
});
