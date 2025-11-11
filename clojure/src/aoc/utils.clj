(ns aoc.utils
  "General utility functions for Advent of Code.")

(defn print-solution
  "Print a formatted solution for a given part.

   Parameters:
   - part: Part number (1 or 2)
   - answer: The answer to print

   Returns: nil (prints to stdout)"
  [part answer]
  (println (str "Part " part ": " answer)))

(defn count-if
  "Count elements in a collection that satisfy a predicate.

   Parameters:
   - pred: Predicate function
   - coll: Collection

   Returns: Integer count"
  [pred coll]
  (count (filter pred coll)))

(defn frequencies-by
  "Build a frequency map using a key function.

   Parameters:
   - key-fn: Function to extract the key from each element
   - coll: Collection

   Returns: Map of key to frequency"
  [key-fn coll]
  (frequencies (map key-fn coll)))

(defn group-by-key
  "Group elements by a key function (alias for group-by for consistency).

   Parameters:
   - key-fn: Function to extract the key from each element
   - coll: Collection

   Returns: Map of key to sequence of elements with that key"
  [key-fn coll]
  (group-by key-fn coll))

(defn parse-int
  "Parse a string to an integer.

   Parameters:
   - s: String to parse

   Returns: Integer, or nil if parsing fails"
  [s]
  (try
    (Integer/parseInt s)
    (catch NumberFormatException _ nil)))

(defn parse-long
  "Parse a string to a long.

   Parameters:
   - s: String to parse

   Returns: Long, or nil if parsing fails"
  [s]
  (try
    (Long/parseLong s)
    (catch NumberFormatException _ nil)))

(defn str->int
  "Parse a string to an integer (throws on failure).

   Parameters:
   - s: String to parse

   Returns: Integer"
  [s]
  (Integer/parseInt s))

(defn transpose
  "Transpose a matrix (sequence of sequences).

   Parameters:
   - matrix: Sequence of sequences

   Returns: Transposed matrix"
  [matrix]
  (apply mapv vector matrix))

(defn range-inclusive
  "Create an inclusive range from start to end.

   Parameters:
   - start: Start value
   - end: End value (inclusive)

   Returns: Lazy sequence"
  [start end]
  (range start (inc end)))

(defn split-at-pred
  "Split a sequence at positions where predicate is true.

   Parameters:
   - pred: Predicate function
   - coll: Collection

   Returns: Sequence of subsequences"
  [pred coll]
  (let [groups (partition-by pred coll)]
    (remove #(pred (first %)) groups)))

(defn fixed-point
  "Apply a function repeatedly until it reaches a fixed point.

   Parameters:
   - f: Function to apply
   - x: Initial value
   - max-iterations: Maximum iterations (optional, default 1000000)

   Returns: Fixed point value"
  ([f x]
   (fixed-point f x 1000000))
  ([f x max-iterations]
   (loop [prev x
          current (f x)
          iterations 0]
     (cond
       (= prev current) current
       (>= iterations max-iterations) (throw (ex-info "Fixed point not reached" {:iterations iterations}))
       :else (recur current (f current) (inc iterations))))))

(defn iterate-until
  "Iterate a function until a predicate is satisfied.

   Parameters:
   - f: Function to apply
   - pred: Predicate to test the result
   - x: Initial value

   Returns: First value satisfying the predicate"
  [f pred x]
  (first (drop-while (complement pred) (iterate f x))))

(defn memoize-with
  "Memoize a function with a custom cache atom.

   Parameters:
   - cache: Atom containing a map for caching
   - f: Function to memoize

   Returns: Memoized function"
  [cache f]
  (fn [& args]
    (if-let [e (find @cache args)]
      (val e)
      (let [ret (apply f args)]
        (swap! cache assoc args ret)
        ret))))

(defn manhattan-distance-1d
  "Calculate Manhattan distance in 1D.

   Parameters:
   - a: First value
   - b: Second value

   Returns: Absolute difference"
  [a b]
  (Math/abs (- a b)))

(defn between?
  "Check if a value is between min and max (inclusive).

   Parameters:
   - x: Value to check
   - min-val: Minimum value
   - max-val: Maximum value

   Returns: Boolean"
  [x min-val max-val]
  (and (>= x min-val) (<= x max-val)))

(defn clamp
  "Clamp a value between min and max.

   Parameters:
   - x: Value to clamp
   - min-val: Minimum value
   - max-val: Maximum value

   Returns: Clamped value"
  [x min-val max-val]
  (max min-val (min max-val x)))

(defn find-first
  "Find the first element in a collection satisfying a predicate.

   Parameters:
   - pred: Predicate function
   - coll: Collection

   Returns: First matching element or nil"
  [pred coll]
  (first (filter pred coll)))

(defn find-index
  "Find the index of the first element satisfying a predicate.

   Parameters:
   - pred: Predicate function
   - coll: Collection

   Returns: Index or nil if not found"
  [pred coll]
  (first (keep-indexed #(when (pred %2) %1) coll)))

(defn update-values
  "Update all values in a map using a function.

   Parameters:
   - f: Function to apply to each value
   - m: Map

   Returns: Map with updated values"
  [f m]
  (into {} (map (fn [[k v]] [k (f v)]) m)))

(defn map-keys
  "Apply a function to all keys in a map.

   Parameters:
   - f: Function to apply to each key
   - m: Map

   Returns: Map with transformed keys"
  [f m]
  (into {} (map (fn [[k v]] [(f k) v]) m)))

(defn map-values
  "Apply a function to all values in a map (alias for update-values).

   Parameters:
   - f: Function to apply to each value
   - m: Map

   Returns: Map with transformed values"
  [f m]
  (update-values f m))

(defn take-until
  "Take elements from a collection until predicate is satisfied (inclusive).

   Parameters:
   - pred: Predicate function
   - coll: Collection

   Returns: Sequence of elements up to and including first match"
  [pred coll]
  (lazy-seq
   (when-let [s (seq coll)]
     (let [x (first s)]
       (cons x (when-not (pred x)
                 (take-until pred (rest s))))))))

(defn min-by
  "Find the element with the minimum value according to a key function.

   Parameters:
   - key-fn: Function to extract comparison value
   - coll: Collection

   Returns: Element with minimum key value"
  [key-fn coll]
  (when (seq coll)
    (reduce (fn [min-elem elem]
              (if (< (key-fn elem) (key-fn min-elem))
                elem
                min-elem))
            coll)))

(defn max-by
  "Find the element with the maximum value according to a key function.

   Parameters:
   - key-fn: Function to extract comparison value
   - coll: Collection

   Returns: Element with maximum key value"
  [key-fn coll]
  (when (seq coll)
    (reduce (fn [max-elem elem]
              (if (> (key-fn elem) (key-fn max-elem))
                elem
                max-elem))
            coll)))

(defn distinct-by
  "Return distinct elements according to a key function.

   Parameters:
   - key-fn: Function to extract comparison key
   - coll: Collection

   Returns: Sequence of distinct elements"
  [key-fn coll]
  (map first (vals (group-by key-fn coll))))

(defn index-by
  "Create a map indexed by a key function.

   Parameters:
   - key-fn: Function to extract the key
   - coll: Collection

   Returns: Map from key to element"
  [key-fn coll]
  (into {} (map (fn [x] [(key-fn x) x]) coll)))
