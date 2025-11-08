/**
 * Tests for Directions class
 */

import { describe, it, expect } from '@jest/globals';
import { Directions } from '../aoc-helpers.js';

describe('Directions', () => {
  describe('Direction constants', () => {
    it('should have correct NORTH direction', () => {
      expect(Directions.NORTH).toEqual([0, -1]);
    });

    it('should have correct EAST direction', () => {
      expect(Directions.EAST).toEqual([1, 0]);
    });

    it('should have correct SOUTH direction', () => {
      expect(Directions.SOUTH).toEqual([0, 1]);
    });

    it('should have correct WEST direction', () => {
      expect(Directions.WEST).toEqual([-1, 0]);
    });
  });

  describe('CARDINAL array', () => {
    it('should contain 4 directions', () => {
      expect(Directions.CARDINAL).toHaveLength(4);
    });

    it('should contain all cardinal directions', () => {
      expect(Directions.CARDINAL).toContainEqual([0, -1]); // N
      expect(Directions.CARDINAL).toContainEqual([1, 0]); // E
      expect(Directions.CARDINAL).toContainEqual([0, 1]); // S
      expect(Directions.CARDINAL).toContainEqual([-1, 0]); // W
    });
  });

  describe('ALL_8 array', () => {
    it('should contain 8 directions', () => {
      expect(Directions.ALL_8).toHaveLength(8);
    });

    it('should contain all 8 directions', () => {
      expect(Directions.ALL_8).toContainEqual([0, -1]); // N
      expect(Directions.ALL_8).toContainEqual([1, -1]); // NE
      expect(Directions.ALL_8).toContainEqual([1, 0]); // E
      expect(Directions.ALL_8).toContainEqual([1, 1]); // SE
      expect(Directions.ALL_8).toContainEqual([0, 1]); // S
      expect(Directions.ALL_8).toContainEqual([-1, 1]); // SW
      expect(Directions.ALL_8).toContainEqual([-1, 0]); // W
      expect(Directions.ALL_8).toContainEqual([-1, -1]); // NW
    });
  });

  describe('DIRECTION_MAP', () => {
    it('should map N to correct direction', () => {
      expect(Directions.DIRECTION_MAP.N).toEqual([0, -1]);
    });

    it('should map NORTH to correct direction', () => {
      expect(Directions.DIRECTION_MAP.NORTH).toEqual([0, -1]);
    });

    it('should map UP to correct direction', () => {
      expect(Directions.DIRECTION_MAP.UP).toEqual([0, -1]);
    });

    it('should map E to correct direction', () => {
      expect(Directions.DIRECTION_MAP.E).toEqual([1, 0]);
    });

    it('should map EAST to correct direction', () => {
      expect(Directions.DIRECTION_MAP.EAST).toEqual([1, 0]);
    });

    it('should map RIGHT to correct direction', () => {
      expect(Directions.DIRECTION_MAP.RIGHT).toEqual([1, 0]);
    });

    it('should map S to correct direction', () => {
      expect(Directions.DIRECTION_MAP.S).toEqual([0, 1]);
    });

    it('should map SOUTH to correct direction', () => {
      expect(Directions.DIRECTION_MAP.SOUTH).toEqual([0, 1]);
    });

    it('should map DOWN to correct direction', () => {
      expect(Directions.DIRECTION_MAP.DOWN).toEqual([0, 1]);
    });

    it('should map W to correct direction', () => {
      expect(Directions.DIRECTION_MAP.W).toEqual([-1, 0]);
    });

    it('should map WEST to correct direction', () => {
      expect(Directions.DIRECTION_MAP.WEST).toEqual([-1, 0]);
    });

    it('should map LEFT to correct direction', () => {
      expect(Directions.DIRECTION_MAP.LEFT).toEqual([-1, 0]);
    });
  });

  describe('ARROW_MAP', () => {
    it('should map ^ to NORTH', () => {
      expect(Directions.ARROW_MAP['^']).toEqual([0, -1]);
    });

    it('should map > to EAST', () => {
      expect(Directions.ARROW_MAP['>']).toEqual([1, 0]);
    });

    it('should map v to SOUTH', () => {
      expect(Directions.ARROW_MAP['v']).toEqual([0, 1]);
    });

    it('should map < to WEST', () => {
      expect(Directions.ARROW_MAP['<']).toEqual([-1, 0]);
    });
  });

  describe('turnRight', () => {
    it('should turn NORTH to EAST', () => {
      const result = Directions.turnRight(Directions.NORTH);
      expect(result).toEqual(Directions.EAST);
    });

    it('should turn EAST to SOUTH', () => {
      const result = Directions.turnRight(Directions.EAST);
      expect(result).toEqual(Directions.SOUTH);
    });

    it('should turn SOUTH to WEST', () => {
      const result = Directions.turnRight(Directions.SOUTH);
      expect(result).toEqual(Directions.WEST);
    });

    it('should turn WEST to NORTH', () => {
      const result = Directions.turnRight(Directions.WEST);
      expect(result).toEqual(Directions.NORTH);
    });

    it('should complete full rotation after 4 turns', () => {
      let dir = Directions.NORTH;
      dir = Directions.turnRight(dir);
      dir = Directions.turnRight(dir);
      dir = Directions.turnRight(dir);
      dir = Directions.turnRight(dir);

      expect(dir).toEqual(Directions.NORTH);
    });
  });

  describe('turnLeft', () => {
    it('should turn NORTH to WEST', () => {
      const result = Directions.turnLeft(Directions.NORTH);
      expect(result).toEqual(Directions.WEST);
    });

    it('should turn WEST to SOUTH', () => {
      const result = Directions.turnLeft(Directions.WEST);
      expect(result).toEqual(Directions.SOUTH);
    });

    it('should turn SOUTH to EAST', () => {
      const result = Directions.turnLeft(Directions.SOUTH);
      expect(result).toEqual(Directions.EAST);
    });

    it('should turn EAST to NORTH', () => {
      const result = Directions.turnLeft(Directions.EAST);
      expect(result).toEqual(Directions.NORTH);
    });

    it('should complete full rotation after 4 turns', () => {
      let dir = Directions.NORTH;
      dir = Directions.turnLeft(dir);
      dir = Directions.turnLeft(dir);
      dir = Directions.turnLeft(dir);
      dir = Directions.turnLeft(dir);

      expect(dir).toEqual(Directions.NORTH);
    });
  });

  describe('Combined rotations', () => {
    it('should return to original after right then left', () => {
      const original = Directions.NORTH;
      const right = Directions.turnRight(original);
      const back = Directions.turnLeft(right);

      expect(back).toEqual(original);
    });

    it('should return to original after left then right', () => {
      const original = Directions.EAST;
      const left = Directions.turnLeft(original);
      const back = Directions.turnRight(left);

      expect(back).toEqual(original);
    });

    it('should reach opposite direction after 2 right turns', () => {
      const dir = Directions.NORTH;
      const opposite = Directions.turnRight(Directions.turnRight(dir));

      expect(opposite).toEqual(Directions.SOUTH);
    });

    it('should reach opposite direction after 2 left turns', () => {
      const dir = Directions.EAST;
      const opposite = Directions.turnLeft(Directions.turnLeft(dir));

      expect(opposite).toEqual(Directions.WEST);
    });
  });
});
