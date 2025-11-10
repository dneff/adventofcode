#lang racket

;; Advent of Code Input Helper Module
;; Provides utilities for reading and parsing input files

(provide read-lines
         read-file
         read-grid
         read-numbers
         read-sections
         parse-numbers
         parse-integers)

;; Read all lines from a file, with optional whitespace preservation
(define (read-lines filename #:preserve-leading-space? [preserve? #f])
  (with-input-from-file filename
    (lambda ()
      (for/list ([line (in-lines)])
        (if preserve?
            line
            (string-trim line))))))

;; Read entire file as a single string
(define (read-file filename)
  (file->string filename))

;; Read file into a 2D grid as a hash table with (x . y) coordinates
;; Returns a hash where keys are coordinate pairs and values are characters
(define (read-grid filename)
  (define lines (read-lines filename))
  (for*/hash ([y (in-naturals)]
              [line (in-list lines)]
              [x (in-naturals)]
              [char (in-string line)])
    (values (cons x y) char)))

;; Read all lines as integers
(define (read-numbers filename)
  (with-input-from-file filename
    (lambda ()
      (for/list ([line (in-lines)])
        (string->number (string-trim line))))))

;; Read file split by empty lines into sections
(define (read-sections filename)
  (define content (string-trim (read-file filename)))
  (define sections (string-split content "\n\n"))
  (map (lambda (section) (string-split section "\n")) sections))

;; Extract all integers from a string (including negative numbers)
(define (parse-numbers text)
  (map string->number
       (regexp-match* #rx"-?[0-9]+" text)))

;; Alias for parse-numbers
(define parse-integers parse-numbers)
