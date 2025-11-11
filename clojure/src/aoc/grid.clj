(ns aoc.grid
  "2D grid operations for Advent of Code."
  (:require [aoc.point :as point]))

(defn make-grid
  "Create a grid from a sequence of rows.

   Parameters:
   - rows: Sequence of sequences (can be strings or vectors)

   Returns: Vector of vectors"
  [rows]
  (mapv vec rows))

(defn grid-get
  "Get value at a position in the grid.

   Parameters:
   - grid: 2D grid (vector of vectors)
   - point: Point [x y]
   - default: Value to return if out of bounds (optional)

   Returns: Value at position or default"
  ([grid [x y]]
   (get-in grid [y x]))
  ([grid [x y] default]
   (get-in grid [y x] default)))

(defn grid-set
  "Set value at a position in the grid.

   Parameters:
   - grid: 2D grid (vector of vectors)
   - point: Point [x y]
   - value: New value

   Returns: Updated grid"
  [grid [x y] value]
  (assoc-in grid [y x] value))

(defn grid-update
  "Update value at a position using a function.

   Parameters:
   - grid: 2D grid (vector of vectors)
   - point: Point [x y]
   - f: Update function

   Returns: Updated grid"
  [grid [x y] f]
  (update-in grid [y x] f))

(defn grid-width
  "Get the width of the grid.

   Parameters:
   - grid: 2D grid (vector of vectors)

   Returns: Integer width"
  [grid]
  (if (empty? grid)
    0
    (count (first grid))))

(defn grid-height
  "Get the height of the grid.

   Parameters:
   - grid: 2D grid (vector of vectors)

   Returns: Integer height"
  [grid]
  (count grid))

(defn grid-dimensions
  "Get both width and height of the grid.

   Parameters:
   - grid: 2D grid (vector of vectors)

   Returns: Map with :width and :height"
  [grid]
  {:width (grid-width grid)
   :height (grid-height grid)})

(defn in-bounds?
  "Check if a point is within grid boundaries.

   Parameters:
   - grid: 2D grid (vector of vectors)
   - point: Point [x y]

   Returns: Boolean"
  [grid point]
  (point/in-bounds? point (grid-width grid) (grid-height grid)))

(defn grid-neighbors-4
  "Get the 4 cardinal neighbors of a position that are in bounds.

   Parameters:
   - grid: 2D grid (vector of vectors)
   - point: Point [x y]

   Returns: Sequence of neighboring points"
  [grid point]
  (filter #(in-bounds? grid %) (point/neighbors-4 point)))

(defn grid-neighbors-8
  "Get all 8 neighbors of a position that are in bounds.

   Parameters:
   - grid: 2D grid (vector of vectors)
   - point: Point [x y]

   Returns: Sequence of neighboring points"
  [grid point]
  (filter #(in-bounds? grid %) (point/neighbors-8 point)))

(defn find-positions
  "Find all positions in the grid matching a predicate.

   Parameters:
   - grid: 2D grid (vector of vectors)
   - pred: Predicate function taking a value

   Returns: Sequence of points [x y]"
  [grid pred]
  (for [y (range (grid-height grid))
        x (range (grid-width grid))
        :when (pred (grid-get grid [x y]))]
    [x y]))

(defn find-position
  "Find the first position in the grid matching a predicate.

   Parameters:
   - grid: 2D grid (vector of vectors)
   - pred: Predicate function taking a value

   Returns: Point [x y] or nil if not found"
  [grid pred]
  (first (find-positions grid pred)))

(defn grid-positions
  "Get all positions in the grid.

   Parameters:
   - grid: 2D grid (vector of vectors)

   Returns: Sequence of points [x y]"
  [grid]
  (for [y (range (grid-height grid))
        x (range (grid-width grid))]
    [x y]))

(defn grid-map
  "Map a function over all grid values.

   Parameters:
   - f: Function taking a value
   - grid: 2D grid (vector of vectors)

   Returns: New grid with mapped values"
  [f grid]
  (mapv #(mapv f %) grid))

(defn grid-map-indexed
  "Map a function over all grid values with positions.

   Parameters:
   - f: Function taking [x y] and value
   - grid: 2D grid (vector of vectors)

   Returns: New grid with mapped values"
  [f grid]
  (vec (for [y (range (grid-height grid))]
         (vec (for [x (range (grid-width grid))]
                (f [x y] (grid-get grid [x y])))))))

(defn grid-filter
  "Filter grid positions by predicate on values.

   Parameters:
   - pred: Predicate function taking a value
   - grid: 2D grid (vector of vectors)

   Returns: Sequence of [point value] pairs"
  [pred grid]
  (for [pos (grid-positions grid)
        :let [val (grid-get grid pos)]
        :when (pred val)]
    [pos val]))

(defn print-grid
  "Print a grid to stdout.

   Parameters:
   - grid: 2D grid (vector of vectors)

   Returns: nil (prints to stdout)"
  [grid]
  (doseq [row grid]
    (println (apply str row))))

(defn grid-count
  "Count positions in grid matching a predicate.

   Parameters:
   - pred: Predicate function taking a value
   - grid: 2D grid (vector of vectors)

   Returns: Integer count"
  [pred grid]
  (count (find-positions grid pred)))
