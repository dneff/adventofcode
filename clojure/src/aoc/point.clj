(ns aoc.point
  "2D point operations and direction handling for Advent of Code.")

;; Direction constants
(def NORTH [0 -1])
(def SOUTH [0 1])
(def EAST [1 0])
(def WEST [-1 0])
(def NORTH-EAST [1 -1])
(def NORTH-WEST [-1 -1])
(def SOUTH-EAST [1 1])
(def SOUTH-WEST [-1 1])

(def CARDINAL-DIRECTIONS
  "Four cardinal directions: N, E, S, W"
  [NORTH EAST SOUTH WEST])

(def ALL-DIRECTIONS
  "All eight directions including diagonals"
  [NORTH NORTH-EAST EAST SOUTH-EAST SOUTH SOUTH-WEST WEST NORTH-WEST])

(defn point
  "Create a point from x and y coordinates.

   Parameters:
   - x: X coordinate
   - y: Y coordinate

   Returns: Vector [x y]"
  [x y]
  [x y])

(defn add
  "Add two points together.

   Parameters:
   - p1: First point [x y]
   - p2: Second point [x y]

   Returns: New point [x y]"
  [[x1 y1] [x2 y2]]
  [(+ x1 x2) (+ y1 y2)])

(defn subtract
  "Subtract second point from first.

   Parameters:
   - p1: First point [x y]
   - p2: Second point [x y]

   Returns: New point [x y]"
  [[x1 y1] [x2 y2]]
  [(- x1 x2) (- y1 y2)])

(defn scale
  "Multiply a point by a scalar.

   Parameters:
   - p: Point [x y]
   - n: Scalar value

   Returns: New point [x y]"
  [[x y] n]
  [(* x n) (* y n)])

(defn manhattan-distance
  "Calculate Manhattan distance between two points.

   Parameters:
   - p1: First point [x y]
   - p2: Second point [x y]

   Returns: Integer distance"
  [[x1 y1] [x2 y2]]
  (+ (Math/abs (- x1 x2))
     (Math/abs (- y1 y2))))

(defn move
  "Move a point in a given direction.

   Parameters:
   - point: Starting point [x y]
   - direction: Direction vector [dx dy]
   - steps: Number of steps (default 1)

   Returns: New point [x y]"
  ([point direction]
   (move point direction 1))
  ([point direction steps]
   (add point (scale direction steps))))

(defn neighbors-4
  "Get the 4 cardinal neighbors of a point.

   Parameters:
   - p: Point [x y]

   Returns: Sequence of neighboring points"
  [p]
  (map #(add p %) CARDINAL-DIRECTIONS))

(defn neighbors-8
  "Get all 8 neighbors of a point (including diagonals).

   Parameters:
   - p: Point [x y]

   Returns: Sequence of neighboring points"
  [p]
  (map #(add p %) ALL-DIRECTIONS))

(defn rotate-left
  "Rotate a direction vector 90 degrees counter-clockwise.

   Parameters:
   - direction: Direction vector [dx dy]

   Returns: Rotated direction vector"
  [[dx dy]]
  [dy (- dx)])

(defn rotate-right
  "Rotate a direction vector 90 degrees clockwise.

   Parameters:
   - direction: Direction vector [dx dy]

   Returns: Rotated direction vector"
  [[dx dy]]
  [(- dy) dx])

(defn reverse-direction
  "Reverse a direction vector.

   Parameters:
   - direction: Direction vector [dx dy]

   Returns: Reversed direction vector"
  [[dx dy]]
  [(- dx) (- dy)])

(defn in-bounds?
  "Check if a point is within grid boundaries.

   Parameters:
   - point: Point [x y]
   - width: Grid width
   - height: Grid height

   Returns: Boolean"
  [[x y] width height]
  (and (>= x 0) (< x width)
       (>= y 0) (< y height)))
