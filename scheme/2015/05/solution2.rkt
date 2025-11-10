#lang racket

;; Advent of Code 2015 - Day 5, Part 2
;; https://adventofcode.com/2015/day/5
;;
;; Determine which strings are "nice" based on new rules.
;; A nice string must have:
;; 1. A pair of letters that appears twice without overlapping
;; 2. A letter that repeats with exactly one letter between them

(require "../../helpers/input.rkt")
(require "../../helpers/utils.rkt")

;; Input file path
(define INPUT-FILE "../../../aoc-data/2015/5/input")

;; Check if any pair appears twice without overlapping
(define (property-one s)
  (define len (string-length s))
  (for/or ([i (in-range 1 len)])
    (define pair (substring s (- i 1) (+ i 1)))
    (or (string-contains? (substring s 0 (- i 1)) pair)
        (string-contains? (substring s (+ i 1)) pair))))

;; Check if any character repeats with a letter in between
(define (property-two s)
  (define chars (string->list s))
  (for/or ([i (in-range 2 (length chars))])
    (equal? (list-ref chars i) (list-ref chars (- i 2)))))

;; Part 2 solution
(define (solve-part2)
  (define lines (read-lines INPUT-FILE))
  (count-if (lambda (line)
              (and (property-one line)
                   (property-two line)))
            lines))

;; Compute and print the solution for Part 2
(print-solution 2 (solve-part2))
