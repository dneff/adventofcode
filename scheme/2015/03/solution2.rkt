#lang racket

;; Advent of Code 2015 - Day 3, Part 2
;; https://adventofcode.com/2015/day/3
;;
;; Santa and Robo-Santa alternate delivering presents based on directions.
;; Count the number of houses that receive at least one present.

(require "../../helpers/input.rkt")
(require "../../helpers/point.rkt")
(require "../../helpers/utils.rkt")

;; Input file path
(define INPUT-FILE "../../../aoc-data/2015/3/input")

;; Part 2 solution
(define (solve-part2)
  (define path (first (read-lines INPUT-FILE)))
  (define directions (string->list path))

  ;; Track visited houses
  (define visited (mutable-set))
  (set-add! visited (point 0 0))

  ;; Follow directions, alternating between Santa and Robo-Santa
  (for/fold ([santa-loc (point 0 0)]
             [robo-loc (point 0 0)]
             #:result (set-count visited))
            ([dir directions]
             [idx (in-naturals)])
    (define is-santa (even? idx))
    (define current-loc (if is-santa santa-loc robo-loc))
    (define new-loc (point-add current-loc (char->direction dir)))
    (set-add! visited new-loc)
    (if is-santa
        (values new-loc robo-loc)
        (values santa-loc new-loc))))

;; Compute and print the solution for Part 2
(print-solution 2 (solve-part2))
