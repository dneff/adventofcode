#lang racket

;; Advent of Code 2015 - Day 1, Part 2
;; https://adventofcode.com/2015/day/1
;;
;; This script finds the position of the first character in the input
;; that causes Santa to enter the basement (floor -1).

(require "../../helpers/input.rkt")
(require "../../helpers/utils.rkt")

;; Input file path
(define INPUT-FILE "../../../aoc-data/2015/1/input")

;; Part 2 solution
(define (solve-part2)
  (define instructions (first (read-lines INPUT-FILE)))
  (define (char-value c)
    (if (equal? c #\() 1 -1))

  (let loop ([chars (string->list instructions)]
             [floor 0]
             [position 1])
    (cond
      [(null? chars) #f]
      [(= floor -1) (- position 1)]
      [else
       (define new-floor (+ floor (char-value (car chars))))
       (if (= new-floor -1)
           position
           (loop (cdr chars) new-floor (+ position 1)))])))

;; Compute and print the solution for Part 2
(print-solution 2 (solve-part2))
