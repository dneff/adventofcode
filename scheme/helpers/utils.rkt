#lang racket

;; Advent of Code Utils Helper Module
;; Provides functional pattern utilities and solution formatting

(provide print-solution
         count-if
         find-first
         partition-by
         group-by
         frequencies
         range
         repeat
         take-while
         drop-while
         iterate
         fix-point
         memoize
         compose-all
         apply-n)

;; Print formatted solution output
(define (print-solution part answer)
  (printf "Part ~a: ~a\n" part answer))

;; Count elements satisfying predicate
(define (count-if pred lst)
  (length (filter pred lst)))

;; Find first element satisfying predicate
(define (find-first pred lst)
  (findf pred lst))

;; Partition list by predicate changes
(define (partition-by f lst)
  (if (null? lst)
      '()
      (let loop ([current (list (car lst))]
                 [rest (cdr lst)]
                 [current-val (f (car lst))])
        (cond
          [(null? rest)
           (list (reverse current))]
          [(equal? current-val (f (car rest)))
           (loop (cons (car rest) current)
                 (cdr rest)
                 current-val)]
          [else
           (cons (reverse current)
                 (partition-by f rest))]))))

;; Group elements by key function
(define (group-by f lst)
  (foldl (lambda (x acc)
           (define key (f x))
           (hash-set acc key (cons x (hash-ref acc key '()))))
         (hash)
         lst))

;; Count frequencies of elements
(define (frequencies lst)
  (foldl (lambda (x acc)
           (hash-set acc x (add1 (hash-ref acc x 0))))
         (hash)
         lst))

;; Generate range (like Python's range)
(define (range start [end #f] [step 1])
  (if end
      (for/list ([i (in-range start end step)]) i)
      (for/list ([i (in-range start)]) i)))

;; Repeat element n times
(define (repeat n x)
  (make-list n x))

;; Take elements while predicate is true
(define (take-while pred lst)
  (if (or (null? lst) (not (pred (car lst))))
      '()
      (cons (car lst) (take-while pred (cdr lst)))))

;; Drop elements while predicate is true
(define (drop-while pred lst)
  (cond
    [(null? lst) '()]
    [(pred (car lst)) (drop-while pred (cdr lst))]
    [else lst]))

;; Iterate function on initial value, returning infinite sequence
(define (iterate f init)
  (stream-cons init (iterate f (f init))))

;; Find fixed point of function
(define (fix-point f x [tolerance 0.0001])
  (define next (f x))
  (if (< (abs (- next x)) tolerance)
      next
      (fix-point f next tolerance)))

;; Memoize a function
(define (memoize f)
  (define cache (make-hash))
  (lambda args
    (hash-ref! cache args (lambda () (apply f args)))))

;; Compose all functions in a list
(define (compose-all . fns)
  (lambda (x)
    (foldr (lambda (f acc) (f acc)) x fns)))

;; Apply function n times
(define (apply-n f n x)
  (if (zero? n)
      x
      (apply-n f (sub1 n) (f x))))
