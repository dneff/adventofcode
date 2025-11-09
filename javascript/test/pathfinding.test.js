/**
 * Tests for Pathfinding class
 */

import { Pathfinding } from '../aoc-helpers.js';

describe('Pathfinding', () => {
  describe('bfs', () => {
    test('finds simple path in grid', () => {
      const start = [0, 0];
      const goal = [2, 2];
      const getNeighbors = (pos) => {
        const [x, y] = pos;
        const neighbors = [];
        // 3x3 grid, only right and down allowed
        if (x < 2) {
          neighbors.push([x + 1, y]);
        }
        if (y < 2) {
          neighbors.push([x, y + 1]);
        }
        return neighbors;
      };

      const path = Pathfinding.bfs(start, goal, getNeighbors);
      expect(path).not.toBeNull();
      expect(path[0]).toEqual([0, 0]);
      expect(path[path.length - 1]).toEqual([2, 2]);
      expect(path.length).toBe(5); // Shortest path length
    });

    test('returns null when no path exists', () => {
      const start = [0, 0];
      const goal = [2, 2];
      const getNeighbors = () => []; // No neighbors, isolated node

      const path = Pathfinding.bfs(start, goal, getNeighbors);
      expect(path).toBeNull();
    });

    test('handles single node (start equals goal)', () => {
      const start = [5, 5];
      const goal = [5, 5];
      const getNeighbors = () => [];

      const path = Pathfinding.bfs(start, goal, getNeighbors);
      expect(path).toEqual([[5, 5]]);
    });

    test('works with string positions', () => {
      const start = 'A';
      const goal = 'D';
      const graph = {
        A: ['B', 'C'],
        B: ['D'],
        C: ['D'],
        D: [],
      };
      const getNeighbors = (node) => graph[node] || [];

      const path = Pathfinding.bfs(start, goal, getNeighbors);
      expect(path).not.toBeNull();
      expect(path[0]).toBe('A');
      expect(path[path.length - 1]).toBe('D');
      expect(path.length).toBe(3); // A -> B -> D or A -> C -> D
    });

    test('works with complex objects', () => {
      const start = { x: 0, y: 0 };
      const goal = { x: 1, y: 1 };
      const getNeighbors = (pos) => {
        const neighbors = [];
        if (pos.x < 2) {
          neighbors.push({ x: pos.x + 1, y: pos.y });
        }
        if (pos.y < 2) {
          neighbors.push({ x: pos.x, y: pos.y + 1 });
        }
        return neighbors;
      };

      const path = Pathfinding.bfs(start, goal, getNeighbors);
      expect(path).not.toBeNull();
      expect(path.length).toBe(3); // [0,0] -> [1,0] or [0,1] -> [1,1]
    });
  });

  describe('bfsDistance', () => {
    test('finds correct distance in grid', () => {
      const start = [0, 0];
      const goal = [3, 3];
      const getNeighbors = (pos) => {
        const [x, y] = pos;
        const neighbors = [];
        // 4x4 grid with 4-directional movement
        if (x > 0) {
          neighbors.push([x - 1, y]);
        }
        if (x < 3) {
          neighbors.push([x + 1, y]);
        }
        if (y > 0) {
          neighbors.push([x, y - 1]);
        }
        if (y < 3) {
          neighbors.push([x, y + 1]);
        }
        return neighbors;
      };

      const distance = Pathfinding.bfsDistance(start, goal, getNeighbors);
      expect(distance).toBe(6); // Manhattan distance
    });

    test('returns -1 when no path exists', () => {
      const start = [0, 0];
      const goal = [5, 5];
      const getNeighbors = () => []; // Isolated node

      const distance = Pathfinding.bfsDistance(start, goal, getNeighbors);
      expect(distance).toBe(-1);
    });

    test('returns 0 when start equals goal', () => {
      const start = [3, 3];
      const goal = [3, 3];
      const getNeighbors = () => [];

      const distance = Pathfinding.bfsDistance(start, goal, getNeighbors);
      expect(distance).toBe(0);
    });

    test('handles maze with obstacles', () => {
      // Simple 4x4 maze
      // S . . .
      // # # . .
      // . . # .
      // . . . G
      const blocked = new Set(['0,1', '1,1', '2,2']);
      const getNeighbors = (pos) => {
        const [x, y] = pos;
        const candidates = [
          [x - 1, y],
          [x + 1, y],
          [x, y - 1],
          [x, y + 1],
        ];
        return candidates.filter(
          ([nx, ny]) => nx >= 0 && nx < 4 && ny >= 0 && ny < 4 && !blocked.has(`${nx},${ny}`),
        );
      };

      const distance = Pathfinding.bfsDistance([0, 0], [3, 3], getNeighbors);
      expect(distance).toBe(6); // Must go around obstacles
    });
  });

  describe('bfsAll', () => {
    test('finds distances to all reachable nodes', () => {
      const start = [1, 1];
      const getNeighbors = (pos) => {
        const [x, y] = pos;
        const neighbors = [];
        // 3x3 grid
        if (x > 0) {
          neighbors.push([x - 1, y]);
        }
        if (x < 2) {
          neighbors.push([x + 1, y]);
        }
        if (y > 0) {
          neighbors.push([x, y - 1]);
        }
        if (y < 2) {
          neighbors.push([x, y + 1]);
        }
        return neighbors;
      };

      const distances = Pathfinding.bfsAll(start, getNeighbors);
      expect(distances.get(JSON.stringify([1, 1]))).toBe(0);
      expect(distances.get(JSON.stringify([0, 1]))).toBe(1);
      expect(distances.get(JSON.stringify([2, 1]))).toBe(1);
      expect(distances.get(JSON.stringify([1, 0]))).toBe(1);
      expect(distances.get(JSON.stringify([1, 2]))).toBe(1);
      expect(distances.get(JSON.stringify([0, 0]))).toBe(2);
      expect(distances.get(JSON.stringify([2, 2]))).toBe(2);
      expect(distances.size).toBe(9); // All 9 positions in 3x3 grid
    });

    test('only includes reachable nodes', () => {
      const start = [0, 0];
      const getNeighbors = (pos) => {
        const [x, y] = pos;
        // Only go right, creating a line
        return x < 3 ? [[x + 1, y]] : [];
      };

      const distances = Pathfinding.bfsAll(start, getNeighbors);
      expect(distances.size).toBe(4); // [0,0], [1,0], [2,0], [3,0]
      expect(distances.get(JSON.stringify([0, 0]))).toBe(0);
      expect(distances.get(JSON.stringify([3, 0]))).toBe(3);
      expect(distances.get(JSON.stringify([0, 1]))).toBeUndefined(); // Not reachable
    });

    test('handles isolated node', () => {
      const start = 'A';
      const getNeighbors = () => [];

      const distances = Pathfinding.bfsAll(start, getNeighbors);
      expect(distances.size).toBe(1);
      expect(distances.get(JSON.stringify('A'))).toBe(0);
    });
  });

  describe('dijkstra', () => {
    test('finds shortest weighted path', () => {
      const start = 'A';
      const goal = 'D';
      const getNeighbors = (node) => {
        const edges = {
          A: [
            ['B', 1],
            ['C', 4],
          ],
          B: [
            ['C', 2],
            ['D', 5],
          ],
          C: [['D', 1]],
          D: [],
        };
        return edges[node] || [];
      };

      const distance = Pathfinding.dijkstra(start, goal, getNeighbors);
      expect(distance).toBe(4); // A -> B (1) -> C (2) -> D (1) = 4
    });

    test('returns null when no path exists', () => {
      const start = 'A';
      const goal = 'Z';
      const getNeighbors = (node) => {
        return node === 'A' ? [['B', 1]] : [];
      };

      const distance = Pathfinding.dijkstra(start, goal, getNeighbors);
      expect(distance).toBeNull();
    });

    test('returns 0 when start equals goal', () => {
      const start = [5, 5];
      const goal = [5, 5];
      const getNeighbors = () => [];

      const distance = Pathfinding.dijkstra(start, goal, getNeighbors);
      expect(distance).toBe(0);
    });

    test('handles varying costs in grid', () => {
      // Grid where different tiles have different costs
      const start = [0, 0];
      const goal = [2, 0];
      const costs = {
        '0,0': 0,
        '1,0': 10, // Expensive middle path
        '2,0': 0,
        '0,1': 1,
        '1,1': 1,
        '2,1': 1,
      };

      const getNeighbors = (pos) => {
        const [x, y] = pos;
        const candidates = [
          [x + 1, y],
          [x - 1, y],
          [x, y + 1],
          [x, y - 1],
        ];
        return candidates
          .filter(([nx, ny]) => costs[`${nx},${ny}`] !== undefined)
          .map(([nx, ny]) => [[nx, ny], costs[`${nx},${ny}`]]);
      };

      const distance = Pathfinding.dijkstra(start, goal, getNeighbors);
      expect(distance).toBe(3); // 0,0 -> 0,1 (1) -> 1,1 (1) -> 2,1 (1) -> 2,0 (0) = 3
    });

    test('works with coordinate arrays', () => {
      const start = [0, 0];
      const goal = [1, 1];
      const getNeighbors = (pos) => {
        const [x, y] = pos;
        const neighbors = [];
        if (x < 2) {
          neighbors.push([[x + 1, y], 1]);
        }
        if (y < 2) {
          neighbors.push([[x, y + 1], 1]);
        }
        return neighbors;
      };

      const distance = Pathfinding.dijkstra(start, goal, getNeighbors);
      expect(distance).toBe(2);
    });
  });

  describe('dijkstraAll', () => {
    test('finds distances to all reachable nodes', () => {
      const start = 'A';
      const getNeighbors = (node) => {
        const edges = {
          A: [
            ['B', 1],
            ['C', 4],
          ],
          B: [
            ['C', 2],
            ['D', 5],
          ],
          C: [['D', 1]],
          D: [],
        };
        return edges[node] || [];
      };

      const distances = Pathfinding.dijkstraAll(start, getNeighbors);
      expect(distances.get(JSON.stringify('A'))).toBe(0);
      expect(distances.get(JSON.stringify('B'))).toBe(1);
      expect(distances.get(JSON.stringify('C'))).toBe(3); // A -> B -> C
      expect(distances.get(JSON.stringify('D'))).toBe(4); // A -> B -> C -> D
      expect(distances.size).toBe(4);
    });

    test('only includes reachable nodes with weights', () => {
      const start = [0, 0];
      const getNeighbors = (pos) => {
        const [x, y] = pos;
        if (x < 2) {
          return [[[x + 1, y], x + 1]];
        } // Increasing costs
        return [];
      };

      const distances = Pathfinding.dijkstraAll(start, getNeighbors);
      expect(distances.get(JSON.stringify([0, 0]))).toBe(0);
      expect(distances.get(JSON.stringify([1, 0]))).toBe(1);
      expect(distances.get(JSON.stringify([2, 0]))).toBe(3); // 0 + 1 + 2
    });

    test('handles cycles correctly', () => {
      const start = 'A';
      const getNeighbors = (node) => {
        const edges = {
          A: [
            ['B', 1],
            ['C', 3],
          ],
          B: [
            ['C', 1],
            ['A', 1],
          ], // Cycle back to A
          C: [['B', 1]], // Cycle back to B
        };
        return edges[node] || [];
      };

      const distances = Pathfinding.dijkstraAll(start, getNeighbors);
      expect(distances.get(JSON.stringify('A'))).toBe(0);
      expect(distances.get(JSON.stringify('B'))).toBe(1);
      expect(distances.get(JSON.stringify('C'))).toBe(2); // A -> B -> C is shorter than A -> C
    });
  });

  describe('edge cases', () => {
    test('handles large graphs efficiently', () => {
      // Create a 100x100 grid
      const start = [0, 0];
      const goal = [99, 99];
      const getNeighbors = (pos) => {
        const [x, y] = pos;
        const neighbors = [];
        if (x > 0) {
          neighbors.push([x - 1, y]);
        }
        if (x < 99) {
          neighbors.push([x + 1, y]);
        }
        if (y > 0) {
          neighbors.push([x, y - 1]);
        }
        if (y < 99) {
          neighbors.push([x, y + 1]);
        }
        return neighbors;
      };

      const startTime = Date.now();
      const distance = Pathfinding.bfsDistance(start, goal, getNeighbors);
      const endTime = Date.now();

      expect(distance).toBe(198); // Manhattan distance
      expect(endTime - startTime).toBeLessThan(100); // Should be fast
    });

    test('handles negative coordinates', () => {
      const start = [-5, -5];
      const goal = [5, 5];
      const getNeighbors = (pos) => {
        const [x, y] = pos;
        const neighbors = [];
        if (x < 5) {
          neighbors.push([x + 1, y]);
        }
        if (y < 5) {
          neighbors.push([x, y + 1]);
        }
        return neighbors;
      };

      const distance = Pathfinding.bfsDistance(start, goal, getNeighbors);
      expect(distance).toBe(20);
    });
  });
});
