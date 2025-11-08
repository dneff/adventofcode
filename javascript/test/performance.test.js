/**
 * Performance benchmarks for Grid2D and other classes
 */

import { describe, it, expect } from '@jest/globals';
import { Grid2D, Point2D, Pathfinding, Counter2D } from '../aoc-helpers.js';

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

  describe('Pathfinding performance', () => {
    it('should handle BFS on 10000-node graph in under 100ms', () => {
      // Create a 100x100 grid (10,000 nodes)
      const size = 100;
      const getNeighbors = (pos) => {
        const [x, y] = pos;
        const neighbors = [];
        if (x > 0) neighbors.push([x - 1, y]);
        if (x < size - 1) neighbors.push([x + 1, y]);
        if (y > 0) neighbors.push([x, y - 1]);
        if (y < size - 1) neighbors.push([x, y + 1]);
        return neighbors;
      };

      const start = Date.now();
      const distance = Pathfinding.bfsDistance([0, 0], [size - 1, size - 1], getNeighbors);
      const elapsed = Date.now() - start;

      expect(distance).toBe((size - 1) * 2); // Manhattan distance
      expect(elapsed).toBeLessThan(100);

      console.log(`  ✓ BFS on 10000-node graph: ${elapsed}ms`);
    });

    it('should handle bfsAll on large graph efficiently', () => {
      // 50x50 grid = 2500 nodes
      const size = 50;
      const getNeighbors = (pos) => {
        const [x, y] = pos;
        const neighbors = [];
        if (x > 0) neighbors.push([x - 1, y]);
        if (x < size - 1) neighbors.push([x + 1, y]);
        if (y > 0) neighbors.push([x, y - 1]);
        if (y < size - 1) neighbors.push([x, y + 1]);
        return neighbors;
      };

      const start = Date.now();
      const distances = Pathfinding.bfsAll([0, 0], getNeighbors);
      const elapsed = Date.now() - start;

      expect(distances.size).toBe(size * size);
      expect(elapsed).toBeLessThan(100);

      console.log(`  ✓ BFS-all on 2500-node graph: ${elapsed}ms`);
    });

    it('should handle Dijkstra on 1000-node weighted graph in under 200ms', () => {
      // Create a weighted grid (32x32 = 1024 nodes)
      const size = 32;
      const getNeighbors = (pos) => {
        const [x, y] = pos;
        const neighbors = [];
        if (x > 0) neighbors.push([[x - 1, y], 1]);
        if (x < size - 1) neighbors.push([[x + 1, y], 1]);
        if (y > 0) neighbors.push([[x, y - 1], 1]);
        if (y < size - 1) neighbors.push([[x, y + 1], 1]);
        // Add diagonal moves with higher cost
        if (x > 0 && y > 0) neighbors.push([[x - 1, y - 1], 2]);
        if (x < size - 1 && y < size - 1) neighbors.push([[x + 1, y + 1], 2]);
        return neighbors;
      };

      const start = Date.now();
      const distance = Pathfinding.dijkstra([0, 0], [size - 1, size - 1], getNeighbors);
      const elapsed = Date.now() - start;

      expect(distance).toBeLessThanOrEqual((size - 1) * 2);
      expect(elapsed).toBeLessThan(200);

      console.log(`  ✓ Dijkstra on 1000-node graph: ${elapsed}ms`);
    });

    it('should handle dijkstraAll on medium graph efficiently', () => {
      // 30x30 grid with varying costs
      const size = 30;
      const getNeighbors = (pos) => {
        const [x, y] = pos;
        const neighbors = [];
        if (x > 0) neighbors.push([[x - 1, y], 1 + (x % 3)]);
        if (x < size - 1) neighbors.push([[x + 1, y], 1 + (x % 3)]);
        if (y > 0) neighbors.push([[x, y - 1], 1 + (y % 3)]);
        if (y < size - 1) neighbors.push([[x, y + 1], 1 + (y % 3)]);
        return neighbors;
      };

      const start = Date.now();
      const distances = Pathfinding.dijkstraAll([size / 2, size / 2], getNeighbors);
      const elapsed = Date.now() - start;

      expect(distances.size).toBe(size * size);
      expect(elapsed).toBeLessThan(200);

      console.log(`  ✓ Dijkstra-all on 900-node graph: ${elapsed}ms`);
    });

    it('should handle complex graph with cycles efficiently', () => {
      // Build a complex graph with 1000 nodes and cycles
      const numNodes = 1000;
      const getNeighbors = (nodeId) => {
        const neighbors = [];
        // Each node connects to next 5 nodes (creates cycles when wrapping)
        for (let i = 1; i <= 5; i++) {
          neighbors.push([(nodeId + i) % numNodes, i]);
        }
        return neighbors;
      };

      const start = Date.now();
      const distance = Pathfinding.dijkstra(0, numNodes - 1, getNeighbors);
      const elapsed = Date.now() - start;

      expect(distance).toBeLessThan(numNodes);
      expect(elapsed).toBeLessThan(100);

      console.log(`  ✓ Dijkstra on 1000-node cyclic graph: ${elapsed}ms`);
    });
  });

  describe('Counter2D performance', () => {
    it('should handle 100000 coordinate updates efficiently', () => {
      const counter = new Counter2D();

      const start = Date.now();
      for (let i = 0; i < 100000; i++) {
        const x = Math.floor(i / 100);
        const y = i % 100;
        counter.add([x, y]);
      }
      const elapsed = Date.now() - start;

      expect(counter.size).toBe(100000);
      expect(elapsed).toBeLessThan(500);

      console.log(`  ✓ 100000 coordinate updates: ${elapsed}ms`);
    });

    it('should handle repeated position updates efficiently', () => {
      const counter = new Counter2D();

      const start = Date.now();
      for (let i = 0; i < 50000; i++) {
        // Update only 100 different positions repeatedly
        const x = i % 10;
        const y = Math.floor(i / 10) % 10;
        counter.add([x, y]);
      }
      const elapsed = Date.now() - start;

      expect(counter.size).toBe(100);
      expect(elapsed).toBeLessThan(100);

      console.log(`  ✓ 50000 updates to 100 positions: ${elapsed}ms`);
    });

    it('should iterate over large counter efficiently', () => {
      const counter = new Counter2D();
      for (let i = 0; i < 10000; i++) {
        counter.add([i, i * 2], i);
      }

      const start = Date.now();
      let sum = 0;
      for (const [pos, count] of counter) {
        sum += count;
      }
      const elapsed = Date.now() - start;

      expect(elapsed).toBeLessThan(50);

      console.log(`  ✓ Iterate 10000 counter entries: ${elapsed}ms`);
    });

    it('should find max positions quickly', () => {
      const counter = new Counter2D();
      for (let i = 0; i < 10000; i++) {
        counter.add([i, i], Math.floor(Math.random() * 1000));
      }

      const start = Date.now();
      const maxCount = counter.getMaxCount();
      const maxPositions = counter.getMaxPositions();
      const elapsed = Date.now() - start;

      expect(maxCount).toBeGreaterThan(0);
      expect(maxPositions.length).toBeGreaterThan(0);
      expect(elapsed).toBeLessThan(50);

      console.log(`  ✓ Find max in 10000 positions: ${elapsed}ms`);
    });

    it('should filter by threshold efficiently', () => {
      const counter = new Counter2D();
      for (let i = 0; i < 5000; i++) {
        counter.add([i, i], i % 100);
      }

      const start = Date.now();
      const positions = counter.positionsAboveThreshold(50);
      const elapsed = Date.now() - start;

      expect(positions.length).toBeGreaterThan(0);
      expect(elapsed).toBeLessThan(50);

      console.log(`  ✓ Filter 5000 positions by threshold: ${elapsed}ms`);
    });
  });
});
