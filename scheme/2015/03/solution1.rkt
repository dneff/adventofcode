#lang racket

;; Advent of Code 2015 - Day 3: Perfectly Spherical Houses in a Vacuum
;; https://adventofcode.com/2015/day/3
;;
;; Santa delivers presents to houses in a 2D grid based on directions.
;; Count the number of houses that receive at least one present.

(require "../../helpers/input.rkt")
(require "../../helpers/point.rkt")
(require "../../helpers/utils.rkt")

;; Input file path
(define INPUT-FILE "../../../aoc-data/2015/3/input")

;; Part 1 solution
(define (solve-part1)
  (define path (first (read-lines INPUT-FILE)))
  (define directions (string->list path))

  ;; Track visited houses
  (define visited (mutable-set))
  (set-add! visited (point 0 0))

  ;; Follow directions
  (for/fold ([location (point 0 0)])
            ([dir directions])
    (define new-location (point-add location (char->direction dir)))
    (set-add! visited new-location)
    new-location)

  ;; Return count of unique houses
  (set-count visited))

;; Compute and print the answer for part 1
(print-solution 1 (solve-part1))
