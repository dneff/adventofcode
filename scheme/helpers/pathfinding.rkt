#lang racket

;; Advent of Code Pathfinding Helper Module
;; Provides BFS, Dijkstra, and A* implementations

(require data/heap)

(provide bfs
         bfs-all-paths
         dijkstra
         a-star
         reconstruct-path)

;; Breadth-First Search
;; neighbors-fn: function that takes a node and returns list of neighbors
;; start: starting node
;; goal-fn: predicate function or specific goal node
;; Returns: path from start to goal, or #f if no path exists
(define (bfs neighbors-fn start goal-fn)
  (define goal? (if (procedure? goal-fn)
                    goal-fn
                    (lambda (n) (equal? n goal-fn))))
  (define visited (mutable-set))
  (define queue (make-queue))
  (define parent (make-hash))

  (enqueue! queue start)
  (set-add! visited start)

  (let loop ()
    (cond
      [(queue-empty? queue) #f]
      [else
       (define current (dequeue! queue))
       (cond
         [(goal? current)
          (reconstruct-path parent start current)]
         [else
          (for ([neighbor (neighbors-fn current)])
            (unless (set-member? visited neighbor)
              (set-add! visited neighbor)
              (hash-set! parent neighbor current)
              (enqueue! queue neighbor)))
          (loop)])])))

;; BFS that finds all nodes reachable from start
;; Returns: set of all reachable nodes
(define (bfs-all-paths neighbors-fn start)
  (define visited (mutable-set))
  (define queue (make-queue))

  (enqueue! queue start)
  (set-add! visited start)

  (let loop ()
    (cond
      [(queue-empty? queue) visited]
      [else
       (define current (dequeue! queue))
       (for ([neighbor (neighbors-fn current)])
         (unless (set-member? visited neighbor)
           (set-add! visited neighbor)
           (enqueue! queue neighbor)))
       (loop)])))

;; Dijkstra's Algorithm
;; neighbors-fn: function that takes a node and returns list of (neighbor . cost) pairs
;; start: starting node
;; goal: goal node or predicate function
;; Returns: (path . total-cost) or #f if no path exists
(define (dijkstra neighbors-fn start goal)
  (define goal? (if (procedure? goal)
                    goal
                    (lambda (n) (equal? n goal))))
  (define visited (mutable-set))
  (define parent (make-hash))
  (define costs (make-hash))
  (define pq (make-heap (lambda (a b) (< (cdr a) (cdr b)))))

  (hash-set! costs start 0)
  (heap-add! pq (cons start 0))

  (let loop ()
    (cond
      [(zero? (heap-count pq)) #f]
      [else
       (define-values (current current-cost) (apply values (heap-min pq)))
       (heap-remove-min! pq)

       (cond
         [(set-member? visited current)
          (loop)]
         [else
          (set-add! visited current)
          (cond
            [(goal? current)
             (cons (reconstruct-path parent start current) current-cost)]
            [else
             (for ([neighbor-pair (neighbors-fn current)])
               (define neighbor (car neighbor-pair))
               (define edge-cost (cdr neighbor-pair))
               (define new-cost (+ current-cost edge-cost))
               (when (< new-cost (hash-ref costs neighbor +inf.0))
                 (hash-set! costs neighbor new-cost)
                 (hash-set! parent neighbor current)
                 (heap-add! pq (cons neighbor new-cost))))
             (loop)])])])))

;; A* Algorithm
;; neighbors-fn: function that takes a node and returns list of (neighbor . cost) pairs
;; heuristic-fn: function that estimates cost from node to goal
;; start: starting node
;; goal: goal node
;; Returns: (path . total-cost) or #f if no path exists
(define (a-star neighbors-fn heuristic-fn start goal)
  (define visited (mutable-set))
  (define parent (make-hash))
  (define g-score (make-hash))  ; cost from start to node
  (define f-score (make-hash))  ; g-score + heuristic
  (define pq (make-heap (lambda (a b) (< (cdr a) (cdr b)))))

  (hash-set! g-score start 0)
  (hash-set! f-score start (heuristic-fn start goal))
  (heap-add! pq (cons start (hash-ref f-score start)))

  (let loop ()
    (cond
      [(zero? (heap-count pq)) #f]
      [else
       (define-values (current _) (apply values (heap-min pq)))
       (heap-remove-min! pq)

       (cond
         [(equal? current goal)
          (cons (reconstruct-path parent start current)
                (hash-ref g-score current))]
         [(set-member? visited current)
          (loop)]
         [else
          (set-add! visited current)
          (for ([neighbor-pair (neighbors-fn current)])
            (define neighbor (car neighbor-pair))
            (define edge-cost (cdr neighbor-pair))
            (define tentative-g (+ (hash-ref g-score current) edge-cost))
            (when (< tentative-g (hash-ref g-score neighbor +inf.0))
              (hash-set! parent neighbor current)
              (hash-set! g-score neighbor tentative-g)
              (define f (+ tentative-g (heuristic-fn neighbor goal)))
              (hash-set! f-score neighbor f)
              (heap-add! pq (cons neighbor f))))
          (loop)])])))

;; Reconstruct path from parent hash
(define (reconstruct-path parent start goal)
  (let loop ([current goal]
             [path '()])
    (cond
      [(equal? current start)
       (cons start path)]
      [(hash-has-key? parent current)
       (loop (hash-ref parent current) (cons current path))]
      [else
       (cons current path)])))
