(ns aoc.year2015.day03
  "Advent of Code 2015 - Day 3: Perfectly Spherical Houses in a Vacuum
   https://adventofcode.com/2015/day/3"
  (:require [aoc.input :as input]
            [aoc.point :as point]
            [aoc.utils :as utils]))

;; Input file path
(def INPUT-FILE "../../../aoc-data/2015/3/input")

(def direction-map
  "Map characters to direction vectors"
  {\^ point/NORTH
   \v point/SOUTH
   \> point/EAST
   \< point/WEST})

(defn solve-part1
  "Count houses that receive at least one present from Santa."
  []
  (let [path (first (input/read-lines INPUT-FILE))
        directions (map direction-map path)]
    (loop [pos [0 0]
           houses #{[0 0]}
           dirs directions]
      (if (empty? dirs)
        (count houses)
        (let [new-pos (point/add pos (first dirs))]
          (recur new-pos
                 (conj houses new-pos)
                 (rest dirs)))))))

(defn solve-part2
  "Count houses that receive at least one present from Santa or Robo-Santa."
  []
  (let [path (first (input/read-lines INPUT-FILE))
        directions (map direction-map path)
        santa-dirs (take-nth 2 directions)
        robo-dirs (take-nth 2 (rest directions))]
    (letfn [(visit-houses [dirs]
              (loop [pos [0 0]
                     houses #{[0 0]}
                     remaining dirs]
                (if (empty? remaining)
                  houses
                  (let [new-pos (point/add pos (first remaining))]
                    (recur new-pos
                           (conj houses new-pos)
                           (rest remaining))))))]
      (let [santa-houses (visit-houses santa-dirs)
            robo-houses (visit-houses robo-dirs)
            all-houses (clojure.set/union santa-houses robo-houses)]
        (count all-houses)))))

(defn -main []
  (utils/print-solution 1 (solve-part1))
  (utils/print-solution 2 (solve-part2)))
