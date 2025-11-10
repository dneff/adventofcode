#lang racket

;; Advent of Code 2015 - Day 5: Doesn't He Have Intern-Elves For This?
;; https://adventofcode.com/2015/day/5
;;
;; Determine which strings are "nice" based on specific rules.
;; A nice string must have:
;; 1. At least 3 vowels
;; 2. At least one letter that appears twice in a row
;; 3. No forbidden pairs (ab, cd, pq, xy)

(require "../../helpers/input.rkt")
(require "../../helpers/utils.rkt")

;; Input file path
(define INPUT-FILE "../../../aoc-data/2015/5/input")

;; Check if string contains at least 3 vowels
(define (property-one s)
  (define vowels '(#\a #\e #\i #\o #\u))
  (define vowel-count
    (for/sum ([c (string->list s)])
      (if (member c vowels) 1 0)))
  (>= vowel-count 3))

;; Check if at least one letter appears twice in a row
(define (property-two s)
  (define chars (string->list s))
  (for/or ([i (in-range 1 (length chars))])
    (equal? (list-ref chars i) (list-ref chars (- i 1)))))

;; Check if no forbidden pairs are in string
(define (property-three s)
  (define bad-pairs '("ab" "cd" "pq" "xy"))
  (for/and ([pair bad-pairs])
    (not (string-contains? s pair))))

;; Part 1 solution
(define (solve-part1)
  (define lines (read-lines INPUT-FILE))
  (count-if (lambda (line)
              (and (property-one line)
                   (property-two line)
                   (property-three line)))
            lines))

;; Compute and print the answer for part 1
(print-solution 1 (solve-part1))
