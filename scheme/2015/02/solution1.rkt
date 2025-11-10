#lang racket

;; Advent of Code 2015 - Day 2: I Was Told There Would Be No Math
;; https://adventofcode.com/2015/day/2
;;
;; Calculate total wrapping paper needed for presents.
;; Each present needs surface area plus extra (smallest side).

(require "../../helpers/input.rkt")
(require "../../helpers/utils.rkt")
(require "../../helpers/math.rkt")

;; Input file path
(define INPUT-FILE "../../../aoc-data/2015/2/input")

;; Calculate wrapping paper needed for one present
(define (get-wrapping l w h)
  (define sides (list (* l w) (* w h) (* h l)))
  (define wrapping (* 2 (sum sides)))
  (define slack (apply min sides))
  (+ wrapping slack))

;; Part 1 solution
(define (solve-part1)
  (define lines (read-lines INPUT-FILE))
  (define (parse-dimensions line)
    (map string->number (string-split line "x")))

  (for/sum ([line lines])
    (apply get-wrapping (parse-dimensions line))))

;; Compute and print the answer for part 1
(print-solution 1 (solve-part1))
