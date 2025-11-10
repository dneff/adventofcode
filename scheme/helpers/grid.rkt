#lang racket

;; Advent of Code Grid Helper Module
;; Provides utilities for 2D grid operations

(require "point.rkt")

(provide make-grid
         grid-ref
         grid-set!
         grid-contains?
         grid-width
         grid-height
         grid-bounds
         grid-positions
         grid-values
         grid-find
         grid-count
         grid-neighbors-4
         grid-neighbors-8
         grid-in-bounds?
         grid-display)

;; Create a grid from a hash table or list of strings
(define (make-grid [data #hash()])
  (cond
    [(hash? data) data]
    [(list? data)
     (for*/hash ([y (in-naturals)]
                 [line (in-list data)]
                 [x (in-naturals)]
                 [char (in-string line)])
       (values (cons x y) char))]
    [else (error "Invalid grid data type")]))

;; Get value at position in grid
(define (grid-ref grid pos [default #f])
  (hash-ref grid pos default))

;; Set value at position in grid (returns new grid, functional style)
(define (grid-set! grid pos value)
  (hash-set grid pos value))

;; Check if grid contains position
(define (grid-contains? grid pos)
  (hash-has-key? grid pos))

;; Get grid dimensions
(define (grid-width grid)
  (if (hash-empty? grid)
      0
      (add1 (apply max (map point-x (hash-keys grid))))))

(define (grid-height grid)
  (if (hash-empty? grid)
      0
      (add1 (apply max (map point-y (hash-keys grid))))))

;; Get grid bounds as (min-x min-y max-x max-y)
(define (grid-bounds grid)
  (if (hash-empty? grid)
      '(0 0 0 0)
      (let* ([positions (hash-keys grid)]
             [xs (map point-x positions)]
             [ys (map point-y positions)])
        (list (apply min xs) (apply min ys)
              (apply max xs) (apply max ys)))))

;; Get all positions in grid
(define (grid-positions grid)
  (hash-keys grid))

;; Get all values in grid
(define (grid-values grid)
  (hash-values grid))

;; Find all positions where predicate is true
(define (grid-find grid pred)
  (for/list ([(pos value) (in-hash grid)]
             #:when (pred value))
    pos))

;; Count positions where predicate is true
(define (grid-count grid pred)
  (for/sum ([(pos value) (in-hash grid)]
            #:when (pred value))
    1))

;; Get valid neighboring positions (4-directional)
(define (grid-neighbors-4 grid pos)
  (filter (lambda (p) (grid-contains? grid p))
          (point-neighbors-4 pos)))

;; Get valid neighboring positions (8-directional)
(define (grid-neighbors-8 grid pos)
  (filter (lambda (p) (grid-contains? grid p))
          (point-neighbors-8 pos)))

;; Check if position is within grid bounds
(define (grid-in-bounds? grid pos)
  (grid-contains? grid pos))

;; Display grid for debugging
(define (grid-display grid)
  (define-values (min-x min-y max-x max-y) (apply values (grid-bounds grid)))
  (for ([y (in-range min-y (add1 max-y))])
    (for ([x (in-range min-x (add1 max-x))])
      (display (grid-ref grid (cons x y) #\.)))
    (newline)))
