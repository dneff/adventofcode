(ns aoc.year2015.day01
  "Advent of Code 2015 - Day 1: Not Quite Lisp
   https://adventofcode.com/2015/day/1"
  (:require [aoc.input :as input]
            [aoc.utils :as utils]))

;; Input file path
(def INPUT-FILE "../../../aoc-data/2015/1/input")

(defn solve-part1
  "Calculate the final floor Santa ends up on.
   '(' means go up one floor, ')' means go down one floor."
  []
  (let [instructions (first (input/read-lines INPUT-FILE))
        move-map {\( 1, \) -1}]
    (reduce + (map move-map instructions))))

(defn solve-part2
  "Find the position of the first character that causes Santa to enter the basement (floor -1)."
  []
  (let [instructions (first (input/read-lines INPUT-FILE))
        move-map {\( 1, \) -1}]
    (loop [pos 0
           floor 0]
      (if (= floor -1)
        pos
        (recur (inc pos)
               (+ floor (move-map (nth instructions pos))))))))

(defn -main []
  (utils/print-solution 1 (solve-part1))
  (utils/print-solution 2 (solve-part2)))
