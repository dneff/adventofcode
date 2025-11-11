(ns aoc.input
  "File reading and parsing utilities for Advent of Code."
  (:require [clojure.string :as str]
            [clojure.java.io :as io]))

(defn read-lines
  "Read a file and return a sequence of lines.

   Parameters:
   - filepath: Path to the input file (string)

   Returns: Sequence of lines as strings"
  [filepath]
  (with-open [rdr (io/reader filepath)]
    (doall (line-seq rdr))))

(defn read-text
  "Read entire file as a single string.

   Parameters:
   - filepath: Path to the input file (string)

   Returns: File contents as a string"
  [filepath]
  (slurp filepath))

(defn read-grid
  "Read a file as a 2D grid (vector of vectors of characters).

   Parameters:
   - filepath: Path to the input file (string)

   Returns: Vector of vectors of characters"
  [filepath]
  (mapv vec (read-lines filepath)))

(defn parse-numbers
  "Extract all numbers from a string.

   Parameters:
   - text: String to parse

   Returns: Sequence of integers"
  [text]
  (map #(Integer/parseInt %) (re-seq #"-?\d+" text)))

(defn read-blocks
  "Read file and split into blocks separated by blank lines.

   Parameters:
   - filepath: Path to the input file (string)

   Returns: Sequence of blocks, where each block is a sequence of lines"
  [filepath]
  (let [content (read-text filepath)
        blocks (str/split content #"\n\n")]
    (map str/split-lines blocks)))

(defn read-numbers
  "Read file and return all numbers found.

   Parameters:
   - filepath: Path to the input file (string)

   Returns: Sequence of integers"
  [filepath]
  (parse-numbers (read-text filepath)))

(defn read-csv
  "Read a CSV file and return rows as vectors.

   Parameters:
   - filepath: Path to the input file (string)
   - separator: Character separator (default comma)

   Returns: Sequence of vectors"
  ([filepath]
   (read-csv filepath ","))
  ([filepath separator]
   (map #(str/split % (re-pattern separator))
        (read-lines filepath))))
