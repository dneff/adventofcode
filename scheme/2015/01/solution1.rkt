#lang racket

;; Advent of Code 2015 - Day 1: Not Quite Lisp
;; https://adventofcode.com/2015/day/1
;;
;; This script calculates the final floor Santa ends up on after following
;; the instructions in the input file.
;; Each '(' means go up one floor, each ')' means go down one floor.

(require "../../helpers/input.rkt")
(require "../../helpers/utils.rkt")

;; Input file path
(define INPUT-FILE "../../../aoc-data/2015/1/input")

;; Part 1 solution
(define (solve-part1)
  (define instructions (first (read-lines INPUT-FILE)))
  (define (char-value c)
    (if (equal? c #\() 1 -1))
  (foldl + 0 (map char-value (string->list instructions))))

;; Compute and print the answer for part 1
(print-solution 1 (solve-part1))
