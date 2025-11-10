#lang racket

;; Advent of Code Point Helper Module
;; Provides utilities for 2D coordinate handling and direction constants

(provide point
         point-x
         point-y
         point-add
         point-sub
         point-multiply
         point-manhattan-distance
         point-neighbors-4
         point-neighbors-8
         NORTH SOUTH EAST WEST
         NORTHEAST NORTHWEST SOUTHEAST SOUTHWEST
         direction-vectors-4
         direction-vectors-8
         char->direction
         turn-left
         turn-right)

;; Point constructor (using cons pairs for simplicity)
(define (point x y)
  (cons x y))

;; Point accessors
(define (point-x p) (car p))
(define (point-y p) (cdr p))

;; Point arithmetic
(define (point-add p1 p2)
  (point (+ (point-x p1) (point-x p2))
         (+ (point-y p1) (point-y p2))))

(define (point-sub p1 p2)
  (point (- (point-x p1) (point-x p2))
         (- (point-y p1) (point-y p2))))

(define (point-multiply p scalar)
  (point (* (point-x p) scalar)
         (* (point-y p) scalar)))

;; Manhattan distance between two points
(define (point-manhattan-distance p1 p2)
  (+ (abs (- (point-x p1) (point-x p2)))
     (abs (- (point-y p1) (point-y p2)))))

;; Direction constants (cardinal directions)
(define NORTH (point 0 -1))
(define SOUTH (point 0 1))
(define EAST (point 1 0))
(define WEST (point -1 0))

;; Diagonal directions
(define NORTHEAST (point 1 -1))
(define NORTHWEST (point -1 -1))
(define SOUTHEAST (point 1 1))
(define SOUTHWEST (point -1 1))

;; Lists of direction vectors
(define direction-vectors-4 (list NORTH SOUTH EAST WEST))
(define direction-vectors-8 (list NORTH SOUTH EAST WEST
                                   NORTHEAST NORTHWEST SOUTHEAST SOUTHWEST))

;; Get 4-directional neighbors
(define (point-neighbors-4 p)
  (map (lambda (dir) (point-add p dir)) direction-vectors-4))

;; Get 8-directional neighbors
(define (point-neighbors-8 p)
  (map (lambda (dir) (point-add p dir)) direction-vectors-8))

;; Convert character to direction
(define (char->direction c)
  (case c
    [(#\^ #\U #\N) NORTH]
    [(#\v #\D #\S) SOUTH]
    [(#\> #\R #\E) EAST]
    [(#\< #\L #\W) WEST]
    [else (error "Unknown direction character:" c)]))

;; Turn direction 90 degrees left
(define (turn-left dir)
  (cond
    [(equal? dir NORTH) WEST]
    [(equal? dir WEST) SOUTH]
    [(equal? dir SOUTH) EAST]
    [(equal? dir EAST) NORTH]
    [else dir]))

;; Turn direction 90 degrees right
(define (turn-right dir)
  (cond
    [(equal? dir NORTH) EAST]
    [(equal? dir EAST) SOUTH]
    [(equal? dir SOUTH) WEST]
    [(equal? dir WEST) NORTH]
    [else dir]))
