"""
Advent of Code 2025 - Day 9: Movie Theater
https://adventofcode.com/2025/day/9

The movie theater has a big tile floor with an interesting pattern. Elves
here are redecorating the theater by switching out some of the square tiles
in the big grid they form. Some of the tiles are red; the Elves would like
to find the largest rectangle that uses red tiles for two of its opposite
corners. They even have a list of where the red tiles are located in the
grid (your puzzle input).

Part 2
Using two red tiles as opposite corners, what is the largest area of any
rectangle you can make using only red and green tiles?

Strategy:
The input is a sequent of red tile postions that consecutively define the
perimeter of green tiles. Thus any position "inside" this perimeter is a
green tile, including the tiles on the perimeter itself. Outside this
perimeter are non-colored tiles.

For any position, based on ray tracing, we can determine if it is a red or
green tile by counting how many times a ray extending to the right intersects
with the perimeter defined by the red tiles. If the count is odd, the position
is "inside" the perimeter and thus a green tile; if even, it is outside and thus
a non-colored tile.

Let's use the positions to define the horizontal and vertical bounds of the grid.

"""

import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "../../"))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, "../../../../aoc-data/2025/9/input")

# Parse input: each line contains "x,y" coordinates of a red tile
# In Part 2, these red tiles form a perimeter around green tiles
red_tile_positions = [
    (int(x), int(y))
    for line in AoCInput.read_lines(INPUT_FILE)
    for x, y in [line.split(",")]
]

# Calculate the bounding box of all red tiles
vertical_bounds = (
    min(y for x, y in red_tile_positions),
    max(y for x, y in red_tile_positions)
)
horizontal_bounds = (
    min(x for x, y in red_tile_positions),
    max(x for x, y in red_tile_positions)
)

# Build border segments from consecutive red tiles
# The red tiles form a closed perimeter when connected in order
vertical_borders = []    # Vertical line segments (same x, different y)
horizontal_borders = []  # Horizontal line segments (same y, different x)

for i in range(len(red_tile_positions)):
    x1, y1 = red_tile_positions[i]
    x2, y2 = red_tile_positions[(i + 1) % len(red_tile_positions)]

    if x1 == x2:  # Vertical border segment
        vertical_borders.append(((x1, min(y1, y2)), (x2, max(y1, y2))))
    elif y1 == y2:  # Horizontal border segment
        horizontal_borders.append(((min(x1, x2), y1), (max(x1, x2), y2)))


def is_inside(pos):
    """
    Determine if a position is inside or on the perimeter defined by red tiles.

    Uses ray casting algorithm: cast a ray from the point to the right and count
    how many times it intersects the perimeter.
    - Odd intersections: point is inside (green tile area)
    - Even intersections: point is outside (non-colored area)
    - On border: considered inside (red or green tile)

    Args:
        pos: Tuple (x, y) representing the position to check

    Returns:
        True if the position is inside the perimeter or on a border, False otherwise
    """
    x, y = pos

    # Quick check: if outside the bounding box, it's definitely not inside
    if (
        x < horizontal_bounds[0]
        or x > horizontal_bounds[1]
        or y < vertical_bounds[0]
        or y > vertical_bounds[1]
    ):
        return False

    # Check if the point lies on any vertical border segment
    for (x1, y1), (x2, y2) in vertical_borders:
        if x == x1 and min(y1, y2) <= y <= max(y1, y2):
            return True  # Point is on this vertical edge

    # Check if the point lies on any horizontal border segment
    for (x1, y1), (x2, y2) in horizontal_borders:
        if y == y1 and min(x1, x2) <= x <= max(x1, x2):
            return True  # Point is on this horizontal edge

    # Ray casting: count intersections with vertical borders to the right
    # Cast a horizontal ray from (x, y) extending to the right (positive x direction)
    intersection_count = 0

    for (x1, y1), (x2, y2) in vertical_borders:
        # Check if this vertical border is to the right of our point (x1 > x)
        # and if the ray at height y intersects this vertical segment
        if x1 > x and min(y1, y2) <= y <= max(y1, y2):
            intersection_count += 1

    # Odd number of intersections means we're inside
    return intersection_count % 2 == 1


def calculate_valid_rectangle_area(corner1, corner2):
    """
    Calculate rectangle area if valid, or return 0 if invalid.

    A rectangle is valid for Part 2 if:
    1. All four corners are inside or on the perimeter (red/green tiles only)
    2. No border segments cut through the rectangle interior

    This ensures the rectangle contains only red and green tiles, not non-colored tiles.

    Args:
        corner1: Tuple (x, y) representing first corner position
        corner2: Tuple (x, y) representing second corner position

    Returns:
        Integer area in tiles if valid, 0 if invalid
    """
    # Normalize corners to get min/max coordinates
    x1, y1 = min(corner1[0], corner2[0]), min(corner1[1], corner2[1])
    x2, y2 = max(corner1[0], corner2[0]), max(corner1[1], corner2[1])

    # Validate that all four corners are inside or on the boundary
    corners = [(x1, y1), (x1, y2), (x2, y1), (x2, y2)]
    if not all(is_inside(corner) for corner in corners):
        return 0  # Rectangle extends outside the valid area

    # Check if any vertical border cuts through the rectangle interior
    for (bx1, by1), (bx2, by2) in vertical_borders:
        # This vertical border is at x=bx1, spanning y from by1 to by2
        # It cuts through the interior if it's strictly between x1 and x2
        if x1 < bx1 < x2:
            # Check if the border's y-range overlaps with the rectangle's y-range
            border_y_min, border_y_max = min(by1, by2), max(by1, by2)

            # Border cuts through if it overlaps the rectangle's y-range
            # (not just touching at the edges)
            if border_y_min < y2 and border_y_max > y1:
                return 0  # Border cuts through interior

    # Check if any horizontal border cuts through the rectangle interior
    for (bx1, by1), (bx2, by2) in horizontal_borders:
        # This horizontal border is at y=by1, spanning x from bx1 to bx2
        # It cuts through the interior if it's strictly between y1 and y2
        if y1 < by1 < y2:
            # Check if the border's x-range overlaps with the rectangle's x-range
            border_x_min, border_x_max = min(bx1, bx2), max(bx1, bx2)

            # Border cuts through if it overlaps the rectangle's x-range
            # (not just touching at the edges)
            if border_x_min < x2 and border_x_max > x1:
                return 0  # Border cuts through interior

    # Rectangle is valid - calculate and return area
    width = abs(corner1[0] - corner2[0]) + 1
    height = abs(corner1[1] - corner2[1]) + 1
    return width * height


def find_largest_rectangle(red_tile_positions):
    """
    Find the largest rectangle using red tiles as opposite corners.

    For Part 2, the rectangle must contain only red and green tiles (no non-colored tiles).
    This means all corners must be inside the perimeter and no borders can cut through.

    Strategy:
    - Try all pairs of red tiles as potential opposite corners
    - Skip pairs that share the same x or y coordinate (not opposite corners)
    - Validate each rectangle and calculate area (returns 0 if invalid)
    - Return the maximum valid area found

    Args:
        red_tile_positions: List of (x, y) tuples representing red tile locations

    Returns:
        Integer representing the largest valid rectangle area in tiles
    """
    largest_area = 0

    # Try all pairs of red tiles
    for idx1 in range(len(red_tile_positions)):
        for idx2 in range(idx1 + 1, len(red_tile_positions)):
            corner1 = red_tile_positions[idx1]
            corner2 = red_tile_positions[idx2]

            # Skip if tiles are aligned horizontally or vertically
            # (they can't be opposite corners of a rectangle)
            if corner1[0] == corner2[0] or corner1[1] == corner2[1]:
                continue

            # Calculate area (returns 0 if rectangle is invalid)
            area = calculate_valid_rectangle_area(corner1, corner2)
            largest_area = max(largest_area, area)

    return largest_area


AoCUtils.print_solution(2, find_largest_rectangle(red_tile_positions))
