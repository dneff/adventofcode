"""
Advent of Code 2018 - Day 23: Experimental Emergency Teleportation (Part 2)
https://adventofcode.com/2018/day/23

Part 2: Find the coordinates that are in range of the largest number of nanobots.
What is the shortest manhattan distance between any of those points and 0,0,0?

Octree approach:
1. Start with a bounding box containing all nanobots
2. Recursively subdivide space into 8 octants (cubes)
3. For each cube, count how many nanobot ranges it could overlap
4. Use a priority queue to explore the most promising regions first
5. Refine down to single points
6. Among points with max overlaps, find the one closest to origin

"""

import os
import sys


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, "../../../../aoc-data/2018/23/input")
sys.path.append(os.path.join(SCRIPT_DIR, "../../"))

from aoc_helpers import AoCInput, AoCUtils
from collections import defaultdict
import itertools

def manhattan_distance_3d(point1, point2):
    """
    Calculate Manhattan distance between two 3D points.

    Manhattan distance is the sum of absolute differences in each dimension.
    For example: distance from (0,0,0) to (1,2,3) = |1-0| + |2-0| + |3-0| = 6

    Args:
        point1: Tuple of (x, y, z) coordinates
        point2: Tuple of (x, y, z) coordinates

    Returns:
        Integer distance between the two points
    """
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1]) + abs(point1[2] - point2[2])

def parse_input(input_lines):
    """
    Parse nanobot data from input lines.

    Each line format: "pos=<x,y,z>, r=radius"
    Example: "pos=<0,0,0>, r=4"

    Args:
        input_lines: List of strings from input file

    Returns:
        List of tuples: ((x, y, z), signal_radius)
    """
    nanobots = []
    for line in input_lines:
        line = line.strip()
        # Split into position part "pos=<x,y,z>" and radius part "radius_value"
        position_part, radius_part = line.split(", r=")

        # Extract x, y, z from "pos=<x,y,z>" by removing "pos=<" prefix and ">" suffix
        x_str, y_str, z_str = position_part[5:-1].split(",")
        x, y, z = int(x_str), int(y_str), int(z_str)
        position = (x, y, z)

        # Parse signal radius
        signal_radius = int(radius_part)

        nanobots.append((position, signal_radius))
    return nanobots


def find_strongest_nanobot(nanobots):
    """
    Find the nanobot with the largest signal radius.

    The "strongest" nanobot is defined as the one that can transmit
    signals the farthest distance.

    Args:
        nanobots: List of tuples ((x, y, z), signal_radius)

    Returns:
        Tuple: ((x, y, z), signal_radius) of the strongest nanobot
    """
    strongest_nanobot = None
    max_signal_radius = 0

    for nanobot in nanobots:
        position, signal_radius = nanobot
        if signal_radius > max_signal_radius:
            max_signal_radius = signal_radius
            strongest_nanobot = nanobot

    return strongest_nanobot


def create_bot_map(nanobots):
    """
    Create a mapping of each nanobot position to all nanobots within its range.

    For each nanobot, determine which other nanobots (including itself) are
    within signal range based on Manhattan distance.

    This function performs an exhaustive pairwise comparison: O(n²) complexity.

    Args:
        nanobots: List of tuples ((x, y, z), signal_radius)

    Returns:
        Dictionary mapping position tuples to sets of nanobots in range:
        {(x, y, z): {nanobot1, nanobot2, ...}}
    """
    bot_range_map = defaultdict(set)

    # Compare each pair of nanobots to see if they're in range of each other
    for source_nanobot in nanobots:
        source_position, source_radius = source_nanobot
        for target_nanobot in nanobots:
            target_position, target_radius = target_nanobot

            # Calculate distance between the two nanobots
            distance = manhattan_distance_3d(source_position, target_position)

            # Check if target is within source's signal range
            if distance <= source_radius:
                bot_range_map[source_position].add(target_nanobot)

            # Check if source is within target's signal range
            if distance <= target_radius:
                bot_range_map[target_position].add(source_nanobot)

    return bot_range_map

class Box3D:
    """
    Represents a 3D axis-aligned bounding box (cuboid) for octree space partitioning.

    Used to recursively divide 3D space into smaller regions to efficiently search
    for the optimal coordinate that is in range of the maximum number of nanobots.
    """
    def __init__(self, min_x, max_x, min_y, max_y, min_z, max_z):
        """
        Initialize a 3D bounding box.

        Args:
            min_x, max_x: X-axis bounds (inclusive)
            min_y, max_y: Y-axis bounds (inclusive)
            min_z, max_z: Z-axis bounds (inclusive)
        """
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        self.min_z = min_z
        self.max_z = max_z

    def contains(self, point):
        """
        Check if a point lies within this box (inclusive boundaries).

        Args:
            point: Tuple of (x, y, z) coordinates

        Returns:
            True if point is within or on the box boundaries
        """
        x, y, z = point
        return (self.min_x <= x <= self.max_x and
                self.min_y <= y <= self.max_y and
                self.min_z <= z <= self.max_z)

    def nearest_distance_to_point(self, point):
        """
        Calculate the nearest Manhattan distance from the box to a point.

        For each dimension:
        - If the point is within the box's range, distance contribution is 0
        - If the point is outside, distance is to the nearest edge

        If the point is inside the box, total distance is 0.

        Args:
            point: Tuple of (x, y, z) coordinates

        Returns:
            Integer Manhattan distance from box to point
        """
        x, y, z = point

        # Calculate distance contribution for X dimension
        distance_x = 0
        if x < self.min_x:
            distance_x = self.min_x - x  # Point is to the left of box
        elif x > self.max_x:
            distance_x = x - self.max_x  # Point is to the right of box

        # Calculate distance contribution for Y dimension
        distance_y = 0
        if y < self.min_y:
            distance_y = self.min_y - y  # Point is below box
        elif y > self.max_y:
            distance_y = y - self.max_y  # Point is above box

        # Calculate distance contribution for Z dimension
        distance_z = 0
        if z < self.min_z:
            distance_z = self.min_z - z  # Point is in front of box
        elif z > self.max_z:
            distance_z = z - self.max_z  # Point is behind box

        return distance_x + distance_y + distance_z
    
    def bot_in_range_count(self, nanobots):
        """
        Count how many nanobots have ranges that overlap with this box.

        A nanobot's range overlaps the box if the nearest distance from the
        nanobot's position to the box is within its signal radius.

        Args:
            nanobots: List of tuples ((x, y, z), signal_radius)

        Returns:
            Integer count of nanobots whose signal range overlaps this box
        """
        overlapping_count = 0
        for nanobot in nanobots:
            nanobot_position, signal_radius = nanobot
            # Calculate the nearest distance from nanobot to any point in this box
            distance_to_box = self.nearest_distance_to_point(nanobot_position)
            # Check if the nanobot's signal can reach this box
            if distance_to_box <= signal_radius:
                overlapping_count += 1
        return overlapping_count

    def subdivide(self):
        """
        Subdivide the box into 8 smaller boxes (octants).

        This divides the space using the midpoint of each dimension, creating:
        - 2 divisions on X-axis (left/right)
        - 2 divisions on Y-axis (bottom/top)
        - 2 divisions on Z-axis (front/back)
        Total: 2³ = 8 octants

        Returns:
            List of 8 Box3D instances representing the octants, ordered as:
            [lower-left-front, lower-right-front, upper-left-front, upper-right-front,
             lower-left-back, lower-right-back, upper-left-back, upper-right-back]
        """
        # Calculate midpoints for each dimension
        mid_x = (self.min_x + self.max_x) // 2
        mid_y = (self.min_y + self.max_y) // 2
        mid_z = (self.min_z + self.max_z) // 2

        # Create 8 octants by combining all combinations of low/high in each dimension
        return [
            # Front octants (min_z to mid_z)
            Box3D(self.min_x, mid_x, self.min_y, mid_y, self.min_z, mid_z),      # Lower-left-front
            Box3D(mid_x+1, self.max_x, self.min_y, mid_y, self.min_z, mid_z),    # Lower-right-front
            Box3D(self.min_x, mid_x, mid_y+1, self.max_y, self.min_z, mid_z),    # Upper-left-front
            Box3D(mid_x+1, self.max_x, mid_y+1, self.max_y, self.min_z, mid_z),  # Upper-right-front
            # Back octants (mid_z+1 to max_z)
            Box3D(self.min_x, mid_x, self.min_y, mid_y, mid_z+1, self.max_z),    # Lower-left-back
            Box3D(mid_x+1, self.max_x, self.min_y, mid_y, mid_z+1, self.max_z),  # Lower-right-back
            Box3D(self.min_x, mid_x, mid_y+1, self.max_y, mid_z+1, self.max_z),  # Upper-left-back
            Box3D(mid_x+1, self.max_x, mid_y+1, self.max_y, mid_z+1, self.max_z),# Upper-right-back
        ]


def get_min_distance_to_origin(box):
    """
    Calculate the minimum Manhattan distance from any point in the box to origin (0,0,0).

    If the origin is inside the box, the distance is 0.
    Otherwise, find the point in the box closest to origin.

    Args:
        box: Box3D instance

    Returns:
        Integer Manhattan distance from closest point in box to origin
    """
    # For each dimension, find the coordinate closest to 0
    # If 0 is within [min, max], the closest value is 0
    # Otherwise, it's whichever boundary is closer to 0

    def closest_to_zero(min_val, max_val):
        if min_val <= 0 <= max_val:
            return 0
        elif abs(min_val) < abs(max_val):
            return min_val
        else:
            return max_val

    closest_x = closest_to_zero(box.min_x, box.max_x)
    closest_y = closest_to_zero(box.min_y, box.max_y)
    closest_z = closest_to_zero(box.min_z, box.max_z)

    return abs(closest_x) + abs(closest_y) + abs(closest_z)


def main():
    """
    Solve Part 2: Find the coordinates that are in range of the largest number of nanobots.
    What is the shortest manhattan distance between any of those points and 0,0,0?

    Algorithm: Octree-based Branch and Bound Search
    1. Start with a bounding box containing all nanobots
    2. Use a priority queue to explore boxes with most nanobot overlaps first
    3. Subdivide promising boxes into 8 octants recursively
    4. Prune boxes that can't improve the current best solution
    5. Continue until we find the optimal single-point coordinate
    """
    # ===== STEP 1: Read and parse input =====
    input_lines = AoCInput.read_lines(INPUT_FILE)
    nanobots = parse_input(input_lines)

    # Build a map of which nanobots are in range of each nanobot
    # (This map is created but not used in the final solution)
    bot_range_map = create_bot_map(nanobots)

    # ===== STEP 2: Initialize search variables =====
    # Track the best position found so far
    max_overlapping_nanobots = 0  # Maximum number of nanobots in range
    best_position = None           # The coordinate with max overlaps

    # ===== STEP 3: Create initial bounding box containing all nanobots =====
    min_x = min(nanobot[0][0] for nanobot in nanobots)
    max_x = max(nanobot[0][0] for nanobot in nanobots)
    min_y = min(nanobot[0][1] for nanobot in nanobots)
    max_y = max(nanobot[0][1] for nanobot in nanobots)
    min_z = min(nanobot[0][2] for nanobot in nanobots)
    max_z = max(nanobot[0][2] for nanobot in nanobots)

    initial_box = Box3D(min_x, max_x, min_y, max_y, min_z, max_z)

    # ===== STEP 4: Initialize priority queue for octree search =====
    import heapq
    counter = itertools.count()  # Unique counter for tie-breaking in priority queue
    priority_queue = []

    # Calculate metrics for initial box
    initial_overlap_count = initial_box.bot_in_range_count(nanobots)
    initial_distance_to_origin = get_min_distance_to_origin(initial_box)

    # Priority queue tuple structure: (priority, tie_breaker, box)
    # - priority: (-overlap_count, distance_to_origin) - we want max overlaps, min distance
    # - negative overlap_count because heapq is a min-heap, but we want max overlaps first
    # - distance_to_origin as secondary priority (prefer closer to origin when overlaps equal)
    # - counter for stable sorting when priorities are equal
    heapq.heappush(
        priority_queue,
        (-initial_overlap_count, initial_distance_to_origin, next(counter), initial_box)
    )
    # ===== STEP 5: Octree search with branch and bound pruning =====
    while priority_queue:
        # Pop the most promising box from priority queue
        neg_overlap_count, min_distance_to_origin, _, current_box = heapq.heappop(priority_queue)
        overlap_count = -neg_overlap_count  # Convert back to positive

        # === PRUNING: Early termination if this box can't improve our best solution ===
        if best_position is not None:
            # If this box has fewer overlaps than our best, we're done
            # (all remaining boxes in queue will also have fewer overlaps due to priority ordering)
            if overlap_count < max_overlapping_nanobots:
                break

            # If same overlaps but this box's minimum distance is worse than best, we're done
            if overlap_count == max_overlapping_nanobots:
                best_distance_to_origin = manhattan_distance_3d((0, 0, 0), best_position)
                if min_distance_to_origin > best_distance_to_origin:
                    break

        # === Check if we've refined down to a single point ===
        is_single_point = (current_box.min_x == current_box.max_x and
                          current_box.min_y == current_box.max_y and
                          current_box.min_z == current_box.max_z)

        if is_single_point:
            # This box represents a single coordinate - check if it's the best we've found
            if overlap_count > max_overlapping_nanobots:
                # Found a new best position with more overlaps
                max_overlapping_nanobots = overlap_count
                best_position = (current_box.min_x, current_box.min_y, current_box.min_z)
            elif overlap_count == max_overlapping_nanobots:
                # Tie in overlaps - choose the one closer to origin
                current_distance = abs(current_box.min_x) + abs(current_box.min_y) + abs(current_box.min_z)
                best_distance = abs(best_position[0]) + abs(best_position[1]) + abs(best_position[2])
                if current_distance < best_distance:
                    best_position = (current_box.min_x, current_box.min_y, current_box.min_z)
        else:
            # === Box contains multiple points - subdivide into 8 octants ===
            for octant in current_box.subdivide():
                # Calculate how many nanobots overlap this octant
                octant_overlap_count = octant.bot_in_range_count(nanobots)

                # PRUNING: Only explore octants that could potentially improve our solution
                # Skip octants with fewer overlaps than our current best
                if octant_overlap_count >= max_overlapping_nanobots or max_overlapping_nanobots == 0:
                    octant_distance = get_min_distance_to_origin(octant)
                    heapq.heappush(
                        priority_queue,
                        (-octant_overlap_count, octant_distance, next(counter), octant)
                    )

    # ===== STEP 6: Output the result =====
    final_distance = manhattan_distance_3d((0, 0, 0), best_position)
    AoCUtils.print_solution(2, final_distance)

if __name__ == "__main__":
    main()
