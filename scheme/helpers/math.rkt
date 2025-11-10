#lang racket

;; Advent of Code Math Helper Module
;; Provides mathematical utilities for common AoC operations

(provide gcd
         lcm
         lcm-list
         factorial
         combinations
         permutations
         divisors
         prime?
         primes-up-to
         manhattan-distance
         mod-pow
         chinese-remainder
         digits
         digits->number
         sum
         product)

;; GCD (already built-in, re-export for completeness)
;; (gcd is already provided by racket)

;; LCM (already built-in, re-export for completeness)
;; (lcm is already provided by racket)

;; LCM for a list of numbers
(define (lcm-list nums)
  (foldl lcm 1 nums))

;; Factorial
(define (factorial n)
  (if (<= n 1)
      1
      (* n (factorial (- n 1)))))

;; Combinations (n choose k)
(define (combinations n k)
  (/ (factorial n)
     (* (factorial k) (factorial (- n k)))))

;; Permutations (n P k)
(define (permutations n k)
  (/ (factorial n)
     (factorial (- n k))))

;; Get all divisors of a number
(define (divisors n)
  (for/list ([i (in-range 1 (add1 n))]
             #:when (zero? (modulo n i)))
    i))

;; Check if a number is prime
(define (prime? n)
  (cond
    [(<= n 1) #f]
    [(<= n 3) #t]
    [(or (zero? (modulo n 2)) (zero? (modulo n 3))) #f]
    [else
     (for/and ([i (in-range 5 (add1 (sqrt n)) 6)])
       (and (not (zero? (modulo n i)))
            (not (zero? (modulo n (+ i 2))))))]))

;; Generate all primes up to n using Sieve of Eratosthenes
(define (primes-up-to n)
  (define sieve (make-vector (add1 n) #t))
  (vector-set! sieve 0 #f)
  (vector-set! sieve 1 #f)
  (for* ([i (in-range 2 (add1 (sqrt n)))]
         #:when (vector-ref sieve i)
         [j (in-range (* i i) (add1 n) i)])
    (vector-set! sieve j #f))
  (for/list ([i (in-range 2 (add1 n))]
             #:when (vector-ref sieve i))
    i))

;; Manhattan distance between two points (can also use from point.rkt)
(define (manhattan-distance x1 y1 x2 y2)
  (+ (abs (- x1 x2)) (abs (- y1 y2))))

;; Modular exponentiation (base^exp mod m)
(define (mod-pow base exp m)
  (cond
    [(zero? exp) 1]
    [(even? exp)
     (define half (mod-pow base (/ exp 2) m))
     (modulo (* half half) m)]
    [else
     (modulo (* base (mod-pow base (- exp 1) m)) m)]))

;; Chinese Remainder Theorem (simplified for two congruences)
(define (chinese-remainder n1 a1 n2 a2)
  (define (extended-gcd a b)
    (if (zero? b)
        (values a 1 0)
        (let-values ([(g x y) (extended-gcd b (modulo a b))])
          (values g y (- x (* (quotient a b) y))))))
  (let-values ([(g x y) (extended-gcd n1 n2)])
    (modulo (+ (* a1 n2 y) (* a2 n1 x)) (* n1 n2))))

;; Get digits of a number as a list
(define (digits n)
  (map (lambda (c) (- (char->integer c) (char->integer #\0)))
       (string->list (number->string n))))

;; Convert list of digits to number
(define (digits->number ds)
  (foldl (lambda (d acc) (+ (* acc 10) d)) 0 ds))

;; Sum of a list
(define (sum lst)
  (apply + lst))

;; Product of a list
(define (product lst)
  (apply * lst))
