/**
 * Performance benchmarks for Grid2D and other classes
 */

import { describe, it, expect } from '@jest/globals';
import { Grid2D, Point2D } from '../aoc-helpers.js';

describe('Performance Benchmarks', () => {
  describe('Grid2D performance', () => {
    it('should construct 1000x1000 grid in reasonable time', () => {
      const size = 1000;
      const lines = [];

      for (let i = 0; i < size; i++) {
        lines.push('.'.repeat(size));
      }

      const start = Date.now();
      const grid = new Grid2D(lines);
      const elapsed = Date.now() - start;

      expect(grid.width).toBe(size);
      expect(grid.height).toBe(size);
      expect(grid.size).toBe(size * size);

      // Should construct in under 2 seconds (1M cells)
      expect(elapsed).toBeLessThan(2000);

      console.log(`  ✓ 1000x1000 grid construction: ${elapsed}ms`);
    });

    it('should perform 10000 random lookups quickly', () => {
      const size = 100;
      const lines = [];

      for (let i = 0; i < size; i++) {
        lines.push('x'.repeat(size));
      }

      const grid = new Grid2D(lines);

      const start = Date.now();
      for (let i = 0; i < 10000; i++) {
        const x = Math.floor(Math.random() * size);
        const y = Math.floor(Math.random() * size);
        grid.get(x, y);
      }
      const elapsed = Date.now() - start;

      // Should complete in under 50ms
      expect(elapsed).toBeLessThan(50);

      console.log(`  ✓ 10000 random lookups: ${elapsed}ms`);
    });

    it('should perform 10000 random sets quickly', () => {
      const grid = new Grid2D(['..........']);

      const start = Date.now();
      for (let i = 0; i < 10000; i++) {
        const x = Math.floor(Math.random() * 100);
        const y = Math.floor(Math.random() * 100);
        grid.set(x, y, 'x');
      }
      const elapsed = Date.now() - start;

      // Should complete in under 100ms
      expect(elapsed).toBeLessThan(100);

      console.log(`  ✓ 10000 random sets: ${elapsed}ms`);
    });

    it('should iterate over 100x100 grid quickly', () => {
      const size = 100;
      const lines = [];

      for (let i = 0; i < size; i++) {
        lines.push('x'.repeat(size));
      }

      const grid = new Grid2D(lines);

      const start = Date.now();
      let count = 0;
      for (const [key, value] of grid) {
        count++;
      }
      const elapsed = Date.now() - start;

      expect(count).toBe(size * size);

      // Should iterate in under 50ms
      expect(elapsed).toBeLessThan(50);

      console.log(`  ✓ Iterate 10000 cells: ${elapsed}ms`);
    });

    it('should find positions in 100x100 grid quickly', () => {
      const size = 100;
      const lines = [];

      // Create grid with some 'X' markers
      for (let i = 0; i < size; i++) {
        let line = '.'.repeat(size);
        if (i % 10 === 0) {
          line = 'X' + line.substring(1);
        }
        lines.push(line);
      }

      const grid = new Grid2D(lines);

      const start = Date.now();
      const positions = grid.findPositions('X');
      const elapsed = Date.now() - start;

      expect(positions.length).toBe(10);

      // Should find in under 20ms
      expect(elapsed).toBeLessThan(20);

      console.log(`  ✓ Find positions in 10000 cells: ${elapsed}ms`);
    });

    it('should get adjacent positions efficiently', () => {
      const size = 100;
      const lines = [];

      for (let i = 0; i < size; i++) {
        lines.push('x'.repeat(size));
      }

      const grid = new Grid2D(lines);

      const start = Date.now();
      for (let i = 0; i < 1000; i++) {
        const x = Math.floor(Math.random() * size);
        const y = Math.floor(Math.random() * size);
        grid.getAdjacent(x, y, true);
      }
      const elapsed = Date.now() - start;

      // Should complete in under 30ms
      expect(elapsed).toBeLessThan(30);

      console.log(`  ✓ 1000 adjacent lookups (8-way): ${elapsed}ms`);
    });
  });

  describe('Point2D performance', () => {
    it('should perform vector operations quickly', () => {
      const points = [];
      for (let i = 0; i < 1000; i++) {
        points.push(new Point2D(i, i * 2));
      }

      const start = Date.now();
      for (let i = 0; i < points.length - 1; i++) {
        const sum = points[i].add(points[i + 1]);
        const diff = points[i].subtract(points[i + 1]);
        const dist = points[i].manhattanDistance(points[i + 1]);
      }
      const elapsed = Date.now() - start;

      // Should complete in under 10ms
      expect(elapsed).toBeLessThan(10);

      console.log(`  ✓ 3000 Point2D operations: ${elapsed}ms`);
    });

    it('should convert to/from string efficiently', () => {
      const start = Date.now();
      for (let i = 0; i < 10000; i++) {
        const p = new Point2D(i, i * 2);
        const str = p.toString();
        const restored = Point2D.fromString(str);
      }
      const elapsed = Date.now() - start;

      // Should complete in under 20ms
      expect(elapsed).toBeLessThan(20);

      console.log(`  ✓ 10000 Point2D string conversions: ${elapsed}ms`);
    });
  });

  describe('Memory efficiency', () => {
    it('should use Map for better memory with sparse grids', () => {
      // Sparse grid with only a few filled cells
      const grid = new Grid2D(['...']);

      // Add scattered points
      for (let i = 0; i < 100; i++) {
        grid.set(i * 10, i * 10, 'X');
      }

      // Map should only store 103 entries (initial 3 + 100 new)
      // An array-based approach would need 1000x1000 = 1M cells
      expect(grid.size).toBeLessThan(200);

      console.log(`  ✓ Sparse grid uses ${grid.size} cells (not ${grid.width * grid.height})`);
    });
  });
});
