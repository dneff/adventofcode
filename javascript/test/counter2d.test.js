/**
 * Tests for Counter2D class
 */

import { Counter2D, Point2D } from '../aoc-helpers.js';

describe('Counter2D', () => {
  describe('add and get', () => {
    test('adds count to position using array', () => {
      const counter = new Counter2D();
      counter.add([3, 4]);
      expect(counter.get([3, 4])).toBe(1);
    });

    test('adds count to position using Point2D', () => {
      const counter = new Counter2D();
      const point = new Point2D(5, 6);
      counter.add(point);
      expect(counter.get(point)).toBe(1);
    });

    test('adds count to position using string', () => {
      const counter = new Counter2D();
      counter.add('7,8');
      expect(counter.get('7,8')).toBe(1);
    });

    test('adds custom count value', () => {
      const counter = new Counter2D();
      counter.add([1, 2], 5);
      expect(counter.get([1, 2])).toBe(5);
    });

    test('accumulates counts for same position', () => {
      const counter = new Counter2D();
      counter.add([2, 3]);
      counter.add([2, 3]);
      counter.add([2, 3], 3);
      expect(counter.get([2, 3])).toBe(5);
    });

    test('handles negative coordinates', () => {
      const counter = new Counter2D();
      counter.add([-1, -2], 10);
      expect(counter.get([-1, -2])).toBe(10);
    });

    test('returns 0 for non-existent position', () => {
      const counter = new Counter2D();
      expect(counter.get([100, 100])).toBe(0);
    });

    test('handles mixed position formats for same coordinate', () => {
      const counter = new Counter2D();
      counter.add([5, 5], 2);
      counter.add('5,5', 3);
      counter.add(new Point2D(5, 5), 5);
      expect(counter.get([5, 5])).toBe(10);
      expect(counter.get('5,5')).toBe(10);
      expect(counter.get(new Point2D(5, 5))).toBe(10);
    });
  });

  describe('positionsAboveThreshold', () => {
    test('returns positions meeting threshold', () => {
      const counter = new Counter2D();
      counter.add([0, 0], 5);
      counter.add([1, 1], 10);
      counter.add([2, 2], 3);
      counter.add([3, 3], 15);

      const positions = counter.positionsAboveThreshold(10);
      expect(positions).toHaveLength(2);
      expect(positions).toContain('1,1');
      expect(positions).toContain('3,3');
    });

    test('includes positions equal to threshold', () => {
      const counter = new Counter2D();
      counter.add([0, 0], 5);
      counter.add([1, 1], 10);

      const positions = counter.positionsAboveThreshold(10);
      expect(positions).toContain('1,1');
    });

    test('returns empty array when no positions meet threshold', () => {
      const counter = new Counter2D();
      counter.add([0, 0], 1);
      counter.add([1, 1], 2);

      const positions = counter.positionsAboveThreshold(100);
      expect(positions).toEqual([]);
    });

    test('returns empty array for empty counter', () => {
      const counter = new Counter2D();
      const positions = counter.positionsAboveThreshold(1);
      expect(positions).toEqual([]);
    });

    test('handles threshold of 0', () => {
      const counter = new Counter2D();
      counter.add([0, 0], 5);
      counter.add([1, 1], 0);

      // threshold is inclusive (>=), so positions with count >= 0 are included
      const positions = counter.positionsAboveThreshold(0);
      expect(positions).toHaveLength(2);
      expect(positions).toContain('0,0');
      expect(positions).toContain('1,1');
    });
  });

  describe('getMaxCount', () => {
    test('returns maximum count', () => {
      const counter = new Counter2D();
      counter.add([0, 0], 5);
      counter.add([1, 1], 10);
      counter.add([2, 2], 3);

      expect(counter.getMaxCount()).toBe(10);
    });

    test('returns 0 for empty counter', () => {
      const counter = new Counter2D();
      expect(counter.getMaxCount()).toBe(0);
    });

    test('handles single position', () => {
      const counter = new Counter2D();
      counter.add([5, 5], 42);
      expect(counter.getMaxCount()).toBe(42);
    });

    test('handles negative counts', () => {
      const counter = new Counter2D();
      counter.add([0, 0], -5);
      counter.add([1, 1], -10);
      counter.add([2, 2], 3);

      expect(counter.getMaxCount()).toBe(3);
    });
  });

  describe('getMaxPositions', () => {
    test('returns all positions with maximum count', () => {
      const counter = new Counter2D();
      counter.add([0, 0], 10);
      counter.add([1, 1], 5);
      counter.add([2, 2], 10);
      counter.add([3, 3], 3);

      const positions = counter.getMaxPositions();
      expect(positions).toHaveLength(2);
      expect(positions).toContain('0,0');
      expect(positions).toContain('2,2');
    });

    test('returns single position when one maximum', () => {
      const counter = new Counter2D();
      counter.add([0, 0], 5);
      counter.add([1, 1], 10);
      counter.add([2, 2], 3);

      const positions = counter.getMaxPositions();
      expect(positions).toEqual(['1,1']);
    });

    test('returns empty array for empty counter', () => {
      const counter = new Counter2D();
      expect(counter.getMaxPositions()).toEqual([]);
    });

    test('returns all positions when all have same count', () => {
      const counter = new Counter2D();
      counter.add([0, 0], 7);
      counter.add([1, 1], 7);
      counter.add([2, 2], 7);

      const positions = counter.getMaxPositions();
      expect(positions).toHaveLength(3);
    });
  });

  describe('iterator', () => {
    test('iterates over all position-count pairs', () => {
      const counter = new Counter2D();
      counter.add([0, 0], 5);
      counter.add([1, 1], 10);
      counter.add([2, 2], 3);

      const entries = [...counter];
      expect(entries).toHaveLength(3);

      const entriesMap = new Map(entries);
      expect(entriesMap.get('0,0')).toBe(5);
      expect(entriesMap.get('1,1')).toBe(10);
      expect(entriesMap.get('2,2')).toBe(3);
    });

    test('works with for...of loop', () => {
      const counter = new Counter2D();
      counter.add([1, 2], 3);
      counter.add([4, 5], 6);

      const collected = [];
      for (const [pos, count] of counter) {
        collected.push({ pos, count });
      }

      expect(collected).toHaveLength(2);
      expect(collected.some((e) => e.pos === '1,2' && e.count === 3)).toBe(true);
      expect(collected.some((e) => e.pos === '4,5' && e.count === 6)).toBe(true);
    });

    test('empty counter yields nothing', () => {
      const counter = new Counter2D();
      const entries = [...counter];
      expect(entries).toEqual([]);
    });
  });

  describe('forEach', () => {
    test('executes callback for each entry', () => {
      const counter = new Counter2D();
      counter.add([0, 0], 5);
      counter.add([1, 1], 10);

      const collected = [];
      counter.forEach((count, position) => {
        collected.push({ position, count });
      });

      expect(collected).toHaveLength(2);
      expect(collected.some((e) => e.position === '0,0' && e.count === 5)).toBe(true);
      expect(collected.some((e) => e.position === '1,1' && e.count === 10)).toBe(true);
    });

    test('handles empty counter', () => {
      const counter = new Counter2D();
      let callCount = 0;
      counter.forEach(() => {
        callCount++;
      });
      expect(callCount).toBe(0);
    });
  });

  describe('size', () => {
    test('returns number of unique positions', () => {
      const counter = new Counter2D();
      expect(counter.size).toBe(0);

      counter.add([0, 0]);
      expect(counter.size).toBe(1);

      counter.add([1, 1]);
      expect(counter.size).toBe(2);

      counter.add([0, 0], 5); // Same position, shouldn't increase size
      expect(counter.size).toBe(2);
    });

    test('handles large number of positions', () => {
      const counter = new Counter2D();
      for (let i = 0; i < 1000; i++) {
        counter.add([i, i]);
      }
      expect(counter.size).toBe(1000);
    });
  });

  describe('error handling', () => {
    test('throws error for invalid position format', () => {
      const counter = new Counter2D();
      expect(() => counter.add(null)).toThrow('Invalid position format');
      expect(() => counter.add(undefined)).toThrow('Invalid position format');
      expect(() => counter.add(42)).toThrow('Invalid position format');
    });
  });

  describe('real-world scenarios', () => {
    test('tracks visited positions in grid traversal', () => {
      const counter = new Counter2D();
      const path = [
        [0, 0],
        [1, 0],
        [1, 1],
        [0, 1],
        [0, 0],
      ]; // Path that revisits [0,0]

      for (const pos of path) {
        counter.add(pos);
      }

      expect(counter.get([0, 0])).toBe(2);
      expect(counter.get([1, 0])).toBe(1);
      expect(counter.size).toBe(4);
    });

    test('finds hotspots in coordinate data', () => {
      const counter = new Counter2D();

      // Simulate data points with clustering
      const points = [
        [10, 10],
        [10, 10],
        [10, 10],
        [11, 10],
        [11, 10],
        [5, 5],
        [100, 100],
        [100, 100],
        [100, 100],
        [100, 100],
      ];

      for (const point of points) {
        counter.add(point);
      }

      const maxCount = counter.getMaxCount();
      const hotspots = counter.getMaxPositions();

      expect(maxCount).toBe(4);
      expect(hotspots).toEqual(['100,100']);
    });

    test('handles large-scale coordinate counting efficiently', () => {
      const counter = new Counter2D();

      // Add 100,000 coordinate updates
      const startTime = Date.now();
      for (let i = 0; i < 100000; i++) {
        const x = Math.floor(i / 100);
        const y = i % 100;
        counter.add([x, y]);
      }
      const endTime = Date.now();

      expect(counter.size).toBe(100000);
      expect(endTime - startTime).toBeLessThan(1000); // Should complete in under 1 second
    });

    test('analyzes overlapping line segments', () => {
      const counter = new Counter2D();

      // Line from (0,0) to (3,0)
      for (let x = 0; x <= 3; x++) {
        counter.add([x, 0]);
      }

      // Line from (1,0) to (1,3)
      for (let y = 0; y <= 3; y++) {
        counter.add([1, y]);
      }

      // Line from (2,0) to (2,2)
      for (let y = 0; y <= 2; y++) {
        counter.add([2, y]);
      }

      // Check overlaps
      expect(counter.get([1, 0])).toBe(2); // Intersection of first two lines
      expect(counter.get([2, 0])).toBe(2); // Intersection of first and third lines
      expect(counter.positionsAboveThreshold(2)).toHaveLength(2);
    });
  });

  describe('integration with Point2D', () => {
    test('works seamlessly with Point2D objects', () => {
      const counter = new Counter2D();

      const p1 = new Point2D(3, 4);
      const p2 = new Point2D(5, 6);
      const p3 = p1.add(new Point2D(1, 1)); // Creates Point2D(4, 5)

      counter.add(p1);
      counter.add(p2);
      counter.add(p3);
      counter.add(p1); // Add p1 again

      expect(counter.get(p1)).toBe(2);
      expect(counter.get(new Point2D(3, 4))).toBe(2); // Same as p1
      expect(counter.get(p2)).toBe(1);
      expect(counter.get([4, 5])).toBe(1); // Same as p3
      expect(counter.size).toBe(3);
    });

    test('handles Point2D adjacent positions', () => {
      const counter = new Counter2D();
      const center = new Point2D(5, 5);

      // Add center and all adjacent positions
      counter.add(center);
      for (const adj of center.adjacentPositions()) {
        counter.add(adj);
      }

      expect(counter.size).toBe(5); // Center + 4 cardinal directions
      expect(counter.get(center)).toBe(1);
    });
  });
});
