#lang racket

;; Advent of Code 2015 - Day 4, Part 2
;; https://adventofcode.com/2015/day/4
;;
;; Find the lowest positive number that produces an MD5 hash
;; starting with six zeros when combined with the secret key.

(require "../../helpers/input.rkt")
(require "../../helpers/utils.rkt")
(require openssl/md5)

;; Input file path
(define INPUT-FILE "../../../aoc-data/2015/4/input")

;; Check if MD5 hash starts with n zeros
(define (starts-with-zeros? hash n)
  (define prefix (substring hash 0 n))
  (equal? prefix (make-string n #\0)))

;; Part 2 solution
(define (solve-part2)
  (define secret-key (string-trim (first (read-lines INPUT-FILE))))

  (let loop ([suffix 0])
    (define test-str (string-append secret-key (number->string suffix)))
    (define hash (md5 test-str))
    (if (starts-with-zeros? hash 6)
        suffix
        (loop (add1 suffix)))))

;; Compute and print the solution for Part 2
(print-solution 2 (solve-part2))
