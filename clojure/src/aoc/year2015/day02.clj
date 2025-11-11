(ns aoc.year2015.day02
  "Advent of Code 2015 - Day 2: I Was Told There Would Be No Math
   https://adventofcode.com/2015/day/2"
  (:require [aoc.input :as input]
            [aoc.utils :as utils]
            [clojure.string :as str]))

;; Input file path
(def INPUT-FILE "../../../aoc-data/2015/2/input")

(defn parse-dimensions
  "Parse a line like '2x3x4' into [2 3 4]"
  [line]
  (mapv #(Integer/parseInt %) (str/split line #"x")))

(defn wrapping-paper
  "Calculate wrapping paper needed for a box with dimensions [l w h]"
  [[l w h]]
  (let [sides [(* l w) (* w h) (* h l)]
        surface-area (* 2 (reduce + sides))
        slack (apply min sides)]
    (+ surface-area slack)))

(defn ribbon-length
  "Calculate ribbon length needed for a box with dimensions [l w h]"
  [[l w h]]
  (let [perimeters [(+ l w) (+ w h) (+ h l)]
        wrap (* 2 (apply min perimeters))
        bow (* l w h)]
    (+ wrap bow)))

(defn solve-part1
  "Calculate total wrapping paper needed for all presents."
  []
  (let [lines (input/read-lines INPUT-FILE)
        dimensions (map parse-dimensions lines)]
    (reduce + (map wrapping-paper dimensions))))

(defn solve-part2
  "Calculate total ribbon length needed for all presents."
  []
  (let [lines (input/read-lines INPUT-FILE)
        dimensions (map parse-dimensions lines)]
    (reduce + (map ribbon-length dimensions))))

(defn -main []
  (utils/print-solution 1 (solve-part1))
  (utils/print-solution 2 (solve-part2)))
