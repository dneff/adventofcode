/**
 * Tests for Grid2D class
 */

import { describe, it, expect, beforeEach } from '@jest/globals';
import { Grid2D, Point2D, Directions } from '../aoc-helpers.js';

describe('Grid2D', () => {
  describe('Constructor', () => {
    it('should create grid from string array', () => {
      const lines = ['abc', 'def', 'ghi'];
      const grid = new Grid2D(lines);

      expect(grid.get(0, 0)).toBe('a');
      expect(grid.get(1, 0)).toBe('b');
      expect(grid.get(0, 1)).toBe('d');
      expect(grid.get(2, 2)).toBe('i');
    });

    it('should create grid from Map', () => {
      const map = new Map();
      map.set('0,0', 'a');
      map.set('1,0', 'b');
      map.set('0,1', 'c');

      const grid = new Grid2D(map);

      expect(grid.get(0, 0)).toBe('a');
      expect(grid.get(1, 0)).toBe('b');
      expect(grid.get(0, 1)).toBe('c');
    });

    it('should create grid from plain object', () => {
      const obj = {
        '0,0': 'a',
        '1,0': 'b',
        '0,1': 'c',
      };

      const grid = new Grid2D(obj);

      expect(grid.get(0, 0)).toBe('a');
      expect(grid.get(1, 0)).toBe('b');
      expect(grid.get(0, 1)).toBe('c');
    });

    it('should handle empty array', () => {
      const grid = new Grid2D([]);

      expect(grid.width).toBe(0);
      expect(grid.height).toBe(0);
      expect(grid.size).toBe(0);
    });

    it('should handle different line lengths', () => {
      const lines = ['abc', 'de', 'f'];
      const grid = new Grid2D(lines);

      expect(grid.get(0, 0)).toBe('a');
      expect(grid.get(1, 1)).toBe('e');
      expect(grid.get(0, 2)).toBe('f');
      expect(grid.get(2, 1)).toBeUndefined();
    });
  });

  describe('Dimensions', () => {
    it('should calculate correct dimensions for 3x3 grid', () => {
      const lines = ['abc', 'def', 'ghi'];
      const grid = new Grid2D(lines);

      expect(grid.width).toBe(3);
      expect(grid.height).toBe(3);
      expect(grid.getDimensions()).toEqual({ width: 3, height: 3 });
    });

    it('should calculate correct dimensions for rectangular grid', () => {
      const lines = ['abcd', 'efgh'];
      const grid = new Grid2D(lines);

      expect(grid.width).toBe(4);
      expect(grid.height).toBe(2);
    });

    it('should cache dimensions', () => {
      const lines = ['abc'];
      const grid = new Grid2D(lines);

      const dim1 = grid.getDimensions();
      const dim2 = grid.getDimensions();

      expect(dim1).toEqual(dim2);
    });

    it('should update dimensions when adding cells', () => {
      const grid = new Grid2D(['ab']);

      expect(grid.width).toBe(2);
      expect(grid.height).toBe(1);

      grid.set(5, 5, 'x');

      expect(grid.width).toBe(6);
      expect(grid.height).toBe(6);
    });
  });

  describe('Get and Set', () => {
    let grid;

    beforeEach(() => {
      grid = new Grid2D(['abc', 'def']);
    });

    it('should get value by coordinates', () => {
      expect(grid.get(0, 0)).toBe('a');
      expect(grid.get(2, 1)).toBe('f');
    });

    it('should get value by string key', () => {
      expect(grid.get('0,0')).toBe('a');
      expect(grid.get('2,1')).toBe('f');
    });

    it('should get value by Point2D', () => {
      const p = new Point2D(1, 1);
      expect(grid.get(p)).toBe('e');
    });

    it('should return undefined for non-existent position', () => {
      expect(grid.get(10, 10)).toBeUndefined();
    });

    it('should set value by coordinates', () => {
      grid.set(0, 0, 'x');
      expect(grid.get(0, 0)).toBe('x');
    });

    it('should set value by string key', () => {
      grid.set('1,1', 'y');
      expect(grid.get(1, 1)).toBe('y');
    });

    it('should set value by Point2D', () => {
      const p = new Point2D(2, 0);
      grid.set(p, 'z');
      expect(grid.get(2, 0)).toBe('z');
    });

    it('should add new positions', () => {
      grid.set(5, 5, 'new');
      expect(grid.get(5, 5)).toBe('new');
    });
  });

  describe('Has and Delete', () => {
    let grid;

    beforeEach(() => {
      grid = new Grid2D(['abc', 'def']);
    });

    it('should check if position exists by coordinates', () => {
      expect(grid.has(0, 0)).toBe(true);
      expect(grid.has(10, 10)).toBe(false);
    });

    it('should check if position exists by string key', () => {
      expect(grid.has('1,1')).toBe(true);
      expect(grid.has('10,10')).toBe(false);
    });

    it('should check if position exists by Point2D', () => {
      const p1 = new Point2D(2, 1);
      const p2 = new Point2D(10, 10);

      expect(grid.has(p1)).toBe(true);
      expect(grid.has(p2)).toBe(false);
    });

    it('should delete position by coordinates', () => {
      expect(grid.has(1, 1)).toBe(true);
      grid.delete(1, 1);
      expect(grid.has(1, 1)).toBe(false);
    });

    it('should delete position by string key', () => {
      expect(grid.has('0,0')).toBe(true);
      grid.delete('0,0');
      expect(grid.has('0,0')).toBe(false);
    });

    it('should delete position by Point2D', () => {
      const p = new Point2D(2, 0);
      expect(grid.has(p)).toBe(true);
      grid.delete(p);
      expect(grid.has(p)).toBe(false);
    });
  });

  describe('Adjacent positions', () => {
    let grid;

    beforeEach(() => {
      grid = new Grid2D(['abc', 'def', 'ghi']);
    });

    it('should get 4 cardinal neighbors for center position', () => {
      const adjacent = grid.getAdjacent(1, 1, false);

      expect(adjacent).toHaveLength(4);
      expect(adjacent).toContain('1,0'); // N
      expect(adjacent).toContain('2,1'); // E
      expect(adjacent).toContain('1,2'); // S
      expect(adjacent).toContain('0,1'); // W
    });

    it('should get 8 neighbors with diagonals for center position', () => {
      const adjacent = grid.getAdjacent(1, 1, true);

      expect(adjacent).toHaveLength(8);
      expect(adjacent).toContain('1,0'); // N
      expect(adjacent).toContain('2,0'); // NE
      expect(adjacent).toContain('2,1'); // E
      expect(adjacent).toContain('2,2'); // SE
      expect(adjacent).toContain('1,2'); // S
      expect(adjacent).toContain('0,2'); // SW
      expect(adjacent).toContain('0,1'); // W
      expect(adjacent).toContain('0,0'); // NW
    });

    it('should handle corner positions', () => {
      const adjacent = grid.getAdjacent(0, 0, false);

      expect(adjacent).toHaveLength(2);
      expect(adjacent).toContain('1,0'); // E
      expect(adjacent).toContain('0,1'); // S
    });

    it('should handle edge positions', () => {
      const adjacent = grid.getAdjacent(1, 0, false);

      expect(adjacent).toHaveLength(3);
      expect(adjacent).toContain('2,0'); // E
      expect(adjacent).toContain('1,1'); // S
      expect(adjacent).toContain('0,0'); // W
    });

    it('should accept string key', () => {
      const adjacent = grid.getAdjacent('1,1', false);

      expect(adjacent).toHaveLength(4);
    });

    it('should accept Point2D', () => {
      const p = new Point2D(1, 1);
      const adjacent = grid.getAdjacent(p, false);

      expect(adjacent).toHaveLength(4);
    });

    it('should accept Point2D with diagonals flag', () => {
      const p = new Point2D(1, 1);
      const adjacent = grid.getAdjacent(p, true);

      expect(adjacent).toHaveLength(8);
    });
  });

  describe('Find positions', () => {
    it('should find all positions with specific value', () => {
      const grid = new Grid2D(['abc', 'dae', 'fga']);

      const positions = grid.findPositions('a');

      expect(positions).toHaveLength(3);
      expect(positions).toContain('0,0');
      expect(positions).toContain('1,1');
      expect(positions).toContain('2,2');
    });

    it('should return empty array if value not found', () => {
      const grid = new Grid2D(['abc']);

      const positions = grid.findPositions('z');

      expect(positions).toHaveLength(0);
    });

    it('should find single position', () => {
      const grid = new Grid2D(['abc']);

      const positions = grid.findPositions('b');

      expect(positions).toEqual(['1,0']);
    });
  });

  describe('In bounds', () => {
    let grid;

    beforeEach(() => {
      grid = new Grid2D(['abc', 'def']);
    });

    it('should return true for valid coordinates', () => {
      expect(grid.inBounds(0, 0)).toBe(true);
      expect(grid.inBounds(2, 1)).toBe(true);
    });

    it('should return false for invalid coordinates', () => {
      expect(grid.inBounds(10, 10)).toBe(false);
      expect(grid.inBounds(-1, -1)).toBe(false);
    });

    it('should accept string key', () => {
      expect(grid.inBounds('1,1')).toBe(true);
      expect(grid.inBounds('10,10')).toBe(false);
    });

    it('should accept Point2D', () => {
      const p1 = new Point2D(1, 1);
      const p2 = new Point2D(10, 10);

      expect(grid.inBounds(p1)).toBe(true);
      expect(grid.inBounds(p2)).toBe(false);
    });
  });

  describe('Iteration', () => {
    let grid;

    beforeEach(() => {
      grid = new Grid2D(['ab', 'cd']);
    });

    it('should iterate with entries()', () => {
      const entries = Array.from(grid.entries());

      expect(entries).toHaveLength(4);
      expect(entries).toContainEqual(['0,0', 'a']);
      expect(entries).toContainEqual(['1,0', 'b']);
      expect(entries).toContainEqual(['0,1', 'c']);
      expect(entries).toContainEqual(['1,1', 'd']);
    });

    it('should iterate with keys()', () => {
      const keys = Array.from(grid.keys());

      expect(keys).toHaveLength(4);
      expect(keys).toContain('0,0');
      expect(keys).toContain('1,0');
      expect(keys).toContain('0,1');
      expect(keys).toContain('1,1');
    });

    it('should iterate with values()', () => {
      const values = Array.from(grid.values());

      expect(values).toHaveLength(4);
      expect(values).toContain('a');
      expect(values).toContain('b');
      expect(values).toContain('c');
      expect(values).toContain('d');
    });

    it('should be iterable with for...of', () => {
      const entries = [];
      for (const [key, value] of grid) {
        entries.push([key, value]);
      }

      expect(entries).toHaveLength(4);
      expect(entries).toContainEqual(['0,0', 'a']);
    });

    it('should support forEach', () => {
      const entries = [];
      grid.forEach((value, key) => {
        entries.push([key, value]);
      });

      expect(entries).toHaveLength(4);
      expect(entries).toContainEqual(['0,0', 'a']);
    });
  });

  describe('Integration with Point2D and Directions', () => {
    it('should work with Point2D for navigation', () => {
      const grid = new Grid2D(['abc', 'def', 'ghi']);
      const start = new Point2D(1, 1);

      expect(grid.get(start)).toBe('e');

      const north = start.add(new Point2D(...Directions.NORTH));
      expect(grid.get(north)).toBe('b');

      const east = start.add(new Point2D(...Directions.EAST));
      expect(grid.get(east)).toBe('f');
    });

    it('should work with Point2D adjacency', () => {
      const grid = new Grid2D(['abc', 'def', 'ghi']);
      const center = new Point2D(1, 1);

      const adjacent = center.adjacentPositions(false);

      for (const pos of adjacent) {
        expect(grid.has(pos)).toBe(true);
      }
    });
  });

  describe('Performance considerations', () => {
    it('should handle large grids efficiently', () => {
      const size = 100;
      const lines = [];

      for (let i = 0; i < size; i++) {
        lines.push('x'.repeat(size));
      }

      const start = Date.now();
      const grid = new Grid2D(lines);
      const constructTime = Date.now() - start;

      expect(grid.width).toBe(size);
      expect(grid.height).toBe(size);
      expect(grid.size).toBe(size * size);

      // Construction should be reasonably fast (< 100ms for 100x100)
      expect(constructTime).toBeLessThan(100);
    });

    it('should handle large grid lookups efficiently', () => {
      const size = 100;
      const lines = [];

      for (let i = 0; i < size; i++) {
        lines.push('x'.repeat(size));
      }

      const grid = new Grid2D(lines);

      const start = Date.now();
      for (let i = 0; i < 1000; i++) {
        grid.get(50, 50);
      }
      const lookupTime = Date.now() - start;

      // 1000 lookups should be very fast (< 10ms)
      expect(lookupTime).toBeLessThan(10);
    });
  });
});
