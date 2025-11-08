/**
 * Tests for Point2D class
 */

import { describe, it, expect } from '@jest/globals';
import { Point2D } from '../aoc-helpers.js';

describe('Point2D', () => {
  describe('Constructor and basic properties', () => {
    it('should create a point with x and y coordinates', () => {
      const p = new Point2D(3, 4);
      expect(p.x).toBe(3);
      expect(p.y).toBe(4);
    });

    it('should handle negative coordinates', () => {
      const p = new Point2D(-5, -10);
      expect(p.x).toBe(-5);
      expect(p.y).toBe(-10);
    });

    it('should handle zero coordinates', () => {
      const p = new Point2D(0, 0);
      expect(p.x).toBe(0);
      expect(p.y).toBe(0);
    });
  });

  describe('Vector arithmetic', () => {
    it('should add two points', () => {
      const p1 = new Point2D(3, 4);
      const p2 = new Point2D(1, 2);
      const result = p1.add(p2);

      expect(result.x).toBe(4);
      expect(result.y).toBe(6);
    });

    it('should add negative coordinates', () => {
      const p1 = new Point2D(5, 10);
      const p2 = new Point2D(-3, -7);
      const result = p1.add(p2);

      expect(result.x).toBe(2);
      expect(result.y).toBe(3);
    });

    it('should subtract two points', () => {
      const p1 = new Point2D(5, 8);
      const p2 = new Point2D(2, 3);
      const result = p1.subtract(p2);

      expect(result.x).toBe(3);
      expect(result.y).toBe(5);
    });

    it('should subtract to negative values', () => {
      const p1 = new Point2D(2, 3);
      const p2 = new Point2D(5, 8);
      const result = p1.subtract(p2);

      expect(result.x).toBe(-3);
      expect(result.y).toBe(-5);
    });

    it('should not modify original points during arithmetic', () => {
      const p1 = new Point2D(3, 4);
      const p2 = new Point2D(1, 2);

      p1.add(p2);

      expect(p1.x).toBe(3);
      expect(p1.y).toBe(4);
      expect(p2.x).toBe(1);
      expect(p2.y).toBe(2);
    });
  });

  describe('Equality', () => {
    it('should return true for equal points', () => {
      const p1 = new Point2D(3, 4);
      const p2 = new Point2D(3, 4);

      expect(p1.equals(p2)).toBe(true);
    });

    it('should return false for different x coordinates', () => {
      const p1 = new Point2D(3, 4);
      const p2 = new Point2D(5, 4);

      expect(p1.equals(p2)).toBe(false);
    });

    it('should return false for different y coordinates', () => {
      const p1 = new Point2D(3, 4);
      const p2 = new Point2D(3, 6);

      expect(p1.equals(p2)).toBe(false);
    });

    it('should handle negative coordinates in equality', () => {
      const p1 = new Point2D(-3, -4);
      const p2 = new Point2D(-3, -4);

      expect(p1.equals(p2)).toBe(true);
    });
  });

  describe('Manhattan distance', () => {
    it('should calculate distance between two points', () => {
      const p1 = new Point2D(0, 0);
      const p2 = new Point2D(3, 4);

      expect(p1.manhattanDistance(p2)).toBe(7);
    });

    it('should calculate distance with negative coordinates', () => {
      const p1 = new Point2D(-2, -3);
      const p2 = new Point2D(1, 1);

      expect(p1.manhattanDistance(p2)).toBe(7);
    });

    it('should return 0 for same point', () => {
      const p1 = new Point2D(5, 5);
      const p2 = new Point2D(5, 5);

      expect(p1.manhattanDistance(p2)).toBe(0);
    });

    it('should be symmetric', () => {
      const p1 = new Point2D(1, 2);
      const p2 = new Point2D(4, 6);

      expect(p1.manhattanDistance(p2)).toBe(p2.manhattanDistance(p1));
    });
  });

  describe('Adjacent positions', () => {
    it('should return 4 cardinal neighbors', () => {
      const p = new Point2D(5, 5);
      const adjacent = p.adjacentPositions(false);

      expect(adjacent).toHaveLength(4);

      // Check all 4 cardinal directions
      expect(adjacent.some((a) => a.equals(new Point2D(5, 4)))).toBe(true); // N
      expect(adjacent.some((a) => a.equals(new Point2D(6, 5)))).toBe(true); // E
      expect(adjacent.some((a) => a.equals(new Point2D(5, 6)))).toBe(true); // S
      expect(adjacent.some((a) => a.equals(new Point2D(4, 5)))).toBe(true); // W
    });

    it('should return 8 neighbors with diagonals', () => {
      const p = new Point2D(5, 5);
      const adjacent = p.adjacentPositions(true);

      expect(adjacent).toHaveLength(8);

      // Check all 8 directions
      expect(adjacent.some((a) => a.equals(new Point2D(5, 4)))).toBe(true); // N
      expect(adjacent.some((a) => a.equals(new Point2D(6, 4)))).toBe(true); // NE
      expect(adjacent.some((a) => a.equals(new Point2D(6, 5)))).toBe(true); // E
      expect(adjacent.some((a) => a.equals(new Point2D(6, 6)))).toBe(true); // SE
      expect(adjacent.some((a) => a.equals(new Point2D(5, 6)))).toBe(true); // S
      expect(adjacent.some((a) => a.equals(new Point2D(4, 6)))).toBe(true); // SW
      expect(adjacent.some((a) => a.equals(new Point2D(4, 5)))).toBe(true); // W
      expect(adjacent.some((a) => a.equals(new Point2D(4, 4)))).toBe(true); // NW
    });

    it('should work at origin', () => {
      const p = new Point2D(0, 0);
      const adjacent = p.adjacentPositions(false);

      expect(adjacent).toHaveLength(4);
      expect(adjacent.some((a) => a.equals(new Point2D(0, -1)))).toBe(true);
      expect(adjacent.some((a) => a.equals(new Point2D(1, 0)))).toBe(true);
      expect(adjacent.some((a) => a.equals(new Point2D(0, 1)))).toBe(true);
      expect(adjacent.some((a) => a.equals(new Point2D(-1, 0)))).toBe(true);
    });
  });

  describe('Conversion methods', () => {
    it('should convert to tuple', () => {
      const p = new Point2D(3, 4);
      const tuple = p.toTuple();

      expect(tuple).toEqual([3, 4]);
      expect(Array.isArray(tuple)).toBe(true);
    });

    it('should convert to string', () => {
      const p = new Point2D(3, 4);
      const str = p.toString();

      expect(str).toBe('3,4');
    });

    it('should convert negative coordinates to string', () => {
      const p = new Point2D(-5, -10);
      const str = p.toString();

      expect(str).toBe('-5,-10');
    });

    it('should create from string', () => {
      const p = Point2D.fromString('3,4');

      expect(p.x).toBe(3);
      expect(p.y).toBe(4);
    });

    it('should create from string with negative coordinates', () => {
      const p = Point2D.fromString('-5,-10');

      expect(p.x).toBe(-5);
      expect(p.y).toBe(-10);
    });

    it('should round-trip through string conversion', () => {
      const original = new Point2D(7, 13);
      const str = original.toString();
      const restored = Point2D.fromString(str);

      expect(restored.equals(original)).toBe(true);
    });
  });
});
