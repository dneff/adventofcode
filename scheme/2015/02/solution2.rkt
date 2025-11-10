#lang racket

;; Advent of Code 2015 - Day 2, Part 2
;; https://adventofcode.com/2015/day/2
;;
;; Calculate total ribbon needed for presents.
;; Ribbon = smallest perimeter + bow (volume).

(require "../../helpers/input.rkt")
(require "../../helpers/utils.rkt")
(require "../../helpers/math.rkt")

;; Input file path
(define INPUT-FILE "../../../aoc-data/2015/2/input")

;; Calculate ribbon needed for wrapping
(define (get-ribbon l w h)
  (define perimeters (list (+ l w) (+ w h) (+ h l)))
  (* 2 (apply min perimeters)))

;; Calculate bow length (volume)
(define (get-bow l w h)
  (* l w h))

;; Part 2 solution
(define (solve-part2)
  (define lines (read-lines INPUT-FILE))
  (define (parse-dimensions line)
    (map string->number (string-split line "x")))

  (for/sum ([line lines])
    (define dims (parse-dimensions line))
    (define l (first dims))
    (define w (second dims))
    (define h (third dims))
    (+ (get-ribbon l w h) (get-bow l w h))))

;; Compute and print the solution for Part 2
(print-solution 2 (solve-part2))
