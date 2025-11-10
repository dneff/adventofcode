#!/usr/bin/env racket
#lang racket

;;; Verify Advent of Code Scheme solutions against known correct answers.
;;;
;;; This script runs each solution file for a specified year and compares the output
;;; against the answer files stored in aoc-data.
;;;
;;; Usage:
;;;     racket scheme/verify_solutions.rkt [YEAR] [DAY] [OPTIONS]
;;;
;;; Positional Arguments:
;;;     YEAR                      The year to verify (e.g., 2015, 2016, 2017)
;;;     DAY                       The day to verify (1-25)
;;;
;;; Options:
;;;     --year YEAR, -y YEAR      The year to verify (alternative to positional)
;;;     --day DAY, -d DAY         The day to verify (alternative to positional)
;;;     --write-missing, -w       Write solution output to missing answer files
;;;     --help, -h                Show this help message
;;;
;;; Examples:
;;;     racket scheme/verify_solutions.rkt              # Verify all years
;;;     racket scheme/verify_solutions.rkt 2015         # Verify year 2015
;;;     racket scheme/verify_solutions.rkt 2015 20      # Verify year 2015, day 20
;;;     racket scheme/verify_solutions.rkt --year 2015 --day 20 --write-missing
;;;
;;; If no year is specified, all years will be verified.
;;; If no day is specified, all days will be verified.

(require racket/cmdline)

;; ANSI color codes for terminal output
(define GREEN "\033[92m")
(define RED "\033[91m")
(define YELLOW "\033[93m")
(define BLUE "\033[94m")
(define RESET "\033[0m")

;; Get an emoji based on the execution time
(define (get-time-emoji elapsed-time)
  (cond
    [(< elapsed-time 1.0) "⚡"]
    [(< elapsed-time 3.0) "🚀"]
    [(< elapsed-time 10.0) "▶️"]
    [(< elapsed-time 30.0) "🐢"]
    [else "🐌"]))

;; Read the expected answer from aoc-data directory
(define (get-expected-answer day part year base-dir)
  (define answer-file
    (build-path (simplify-path (build-path base-dir "../../aoc-data"))
                (number->string year)
                (number->string day)
                (format "solution-~a" part)))

  (if (file-exists? answer-file)
      (let ([content (string-trim (file->string answer-file))])
        (if (and (not (string=? content ""))
                 (not (string=? content "0")))
            content
            #f))
      #f))

;; Write an answer to the aoc-data directory
(define (write-answer day part year answer base-dir)
  (define answer-dir
    (build-path (simplify-path (build-path base-dir "../../aoc-data"))
                (number->string year)
                (number->string day)))
  (define answer-file (build-path answer-dir (format "solution-~a" part)))

  (with-handlers ([exn:fail? (lambda (e)
                               (printf "~aError writing answer: ~a~a\n"
                                       RED (exn-message e) RESET)
                               #f)])
    (make-directory* answer-dir)
    (display-to-file (string-append (string-trim answer) "\n")
                     answer-file
                     #:exists 'replace)
    #t))

;; Run a solution file and extract the answer
(define (run-solution day part year base-dir)
  (define solution-file
    (build-path base-dir
                (number->string year)
                (format "~a~a" (if (< day 10) "0" "") day)
                (format "solution~a.rkt" part)))

  (if (not (file-exists? solution-file))
      (values #f #f 0.0 #f)
      (with-handlers ([exn:fail? (lambda (e) (values #f #f 0.0 #t))])
        (define start-time (current-inexact-milliseconds))
        (define-values (process stdout stdin stderr)
          (subprocess #f #f #f (find-executable-path "racket") (path->string solution-file)))

        ;; Wait for process to complete (with timeout)
        (define result
          (sync/timeout 30 process))

        (define elapsed-time (/ (- (current-inexact-milliseconds) start-time) 1000.0))

        (cond
          [(not result)
           ;; Timeout
           (subprocess-kill process #t)
           (values #f #f 30.0 #t)]
          [else
           ;; Process completed
           (define output (port->string stdout))
           (close-input-port stdout)
           (close-input-port stderr)
           (close-output-port stdin)

           (if (not (zero? (subprocess-status process)))
               (values #f #f elapsed-time #t)
               ;; Extract answer from output
               (let ([answer (extract-answer output part)])
                 (values answer (if answer #t #f) elapsed-time #t)))]))))

;; Extract the answer from solution output
(define (extract-answer output part)
  (define pattern (format "Part ~a:" part))
  (define lines (string-split output "\n"))
  (for/or ([line lines])
    (if (string-contains? line pattern)
        (string-trim (last (string-split line ":")))
        #f)))

;; Get the list of years to verify
(define (get-years-to-verify base-dir year)
  (if year
      (list year)
      (let ([dirs (filter directory-exists?
                          (map (lambda (f) (build-path base-dir f))
                               (directory-list base-dir)))])
        (sort (filter-map (lambda (d)
                            (define name (path->string (last (explode-path d))))
                            (and (regexp-match? #rx"^[0-9]+$" name)
                                 (string->number name)))
                          dirs)
              <))))

;; Main verification function
(define (verify-solutions year-arg day-arg write-missing?)
  (define base-dir (simplify-path (build-path (find-system-path 'run-file) "..")))
  (define years-to-verify (get-years-to-verify base-dir year-arg))

  (when (null? years-to-verify)
    (printf "~aError: No Scheme solutions directories found~a\n" RED RESET)
    (exit 1))

  ;; Determine days to verify
  (define days-to-verify
    (if day-arg
        (begin
          (unless (<= 1 day-arg 25)
            (printf "~aError: Day must be between 1 and 25~a\n" RED RESET)
            (exit 1))
          (list day-arg))
        (range 1 26)))

  ;; Track overall statistics
  (define-values (all-total-verified all-total-correct all-total-incorrect
                  all-total-missing all-total-failed)
    (for/fold ([all-verified 0] [all-correct 0] [all-incorrect 0]
               [all-missing 0] [all-failed 0])
              ([year years-to-verify])
      (define scheme-year-dir (build-path base-dir (number->string year)))
      (define aoc-data-dir
        (build-path (simplify-path (build-path base-dir "../../aoc-data"))
                    (number->string year)))

      (unless (directory-exists? scheme-year-dir)
        (printf "~aError: Scheme solutions directory not found for year ~a~a\n"
                RED year RESET)
        (printf "Expected directory: ~a\n" scheme-year-dir)
        (values all-verified all-correct all-incorrect all-missing all-failed))

      (when (and (not (directory-exists? aoc-data-dir)) (not write-missing?))
        (printf "~aWarning: aoc-data directory not found for year ~a~a\n"
                YELLOW year RESET)
        (printf "Expected directory: ~a\n" aoc-data-dir)
        (printf "Continuing anyway, but no answers will be verified.\n"))

      (when (> (length years-to-verify) 1)
        (printf "\n"))
      (printf "~aVerifying ~a Advent of Code Solutions~a\n" BLUE year RESET)
      (printf "~a\n" (make-string 60 #\=))

      ;; Track per-year statistics
      (define-values (total-verified total-correct total-incorrect
                      total-missing total-failed total-written)
        (for*/fold ([verified 0] [correct 0] [incorrect 0]
                    [missing 0] [failed 0] [written 0])
                   ([day days-to-verify]
                    [part '(1 2)])
          (define expected (get-expected-answer day part year base-dir))
          (define-values (actual success elapsed-time file-exists)
            (run-solution day part year base-dir))

          ;; Case 1: Solution file doesn't exist and answer file doesn't exist
          (cond
            [(and (not file-exists) (not expected))
             (values verified correct incorrect missing failed written)]

            ;; Case 2: Solution file doesn't exist but answer file exists
            [(and (not file-exists) expected)
             (printf "~a○~a Day ~a Part ~a: ~aMISSING~a (solution file not found)\n"
                     YELLOW RESET (~a day #:width 2 #:align 'right)
                     part YELLOW RESET)
             (values verified correct incorrect (+ missing 1) failed written)]

            ;; Case 3: Solution file exists but failed to run
            [(and file-exists (or (not success) (not actual)))
             (define emoji (get-time-emoji elapsed-time))
             (printf "~a✗~a Day ~a Part ~a: ~aFAILED TO RUN~a (~a~as) ~a\n"
                     RED RESET (~a day #:width 2 #:align 'right)
                     part RED RESET (~r elapsed-time #:precision 3) RESET emoji)
             (values verified correct incorrect missing (+ failed 1) written)]

            ;; Case 4: Solution ran successfully but no expected answer
            [(not expected)
             (define emoji (get-time-emoji elapsed-time))
             (define status-msg
               (if write-missing?
                   (if (write-answer day part year actual base-dir)
                       (format "~aMISSING (wrote: ~a)~a" YELLOW actual RESET)
                       (format "~aMISSING (failed to write)~a" YELLOW RESET))
                   (format "~aMISSING~a" YELLOW RESET)))

             (printf "~a○~a Day ~a Part ~a: ~a (answer: ~a, ~a~as) ~a\n"
                     YELLOW RESET (~a day #:width 2 #:align 'right)
                     part status-msg actual (~r elapsed-time #:precision 3) RESET emoji)
             (values verified correct incorrect (+ missing 1) failed
                     (if (and write-missing? (write-answer day part year actual base-dir))
                         (+ written 1)
                         written))]

            ;; Case 5: Solution ran successfully and has expected answer
            [else
             (define emoji (get-time-emoji elapsed-time))
             (if (string=? actual expected)
                 (begin
                   (printf "~a✓~a Day ~a Part ~a: ~aCORRECT~a (answer: ~a, ~a~as) ~a\n"
                           GREEN RESET (~a day #:width 2 #:align 'right)
                           part GREEN RESET actual (~r elapsed-time #:precision 3) RESET emoji)
                   (values (+ verified 1) (+ correct 1) incorrect missing failed written))
                 (begin
                   (printf "~a✗~a Day ~a Part ~a: ~aINCORRECT~a (expected: ~a, got: ~a, ~a~as) ~a\n"
                           RED RESET (~a day #:width 2 #:align 'right)
                           part RED RESET expected actual (~r elapsed-time #:precision 3) RESET emoji)
                   (values (+ verified 1) correct (+ incorrect 1) missing failed written)))])))

      ;; Print summary for this year
      (printf "\n~a\n" (make-string 60 #\=))
      (printf "~aSummary for ~a:~a\n" BLUE year RESET)
      (printf "  ~aCorrect:~a      ~a\n" GREEN RESET total-correct)
      (printf "  ~aIncorrect:~a    ~a\n" RED RESET total-incorrect)
      (printf "  ~aFailed:~a       ~a\n" RED RESET total-failed)
      (printf "  ~aMissing:~a      ~a\n" YELLOW RESET total-missing)
      (when (and write-missing? (> total-written 0))
        (printf "  ~aWritten:~a      ~a\n" YELLOW RESET total-written))
      (printf "  ~aTotal Verified:~a ~a\n" BLUE RESET total-verified)

      (values (+ all-verified total-verified)
              (+ all-correct total-correct)
              (+ all-incorrect total-incorrect)
              (+ all-missing total-missing)
              (+ all-failed total-failed))))

  ;; Print overall summary if multiple years
  (when (> (length years-to-verify) 1)
    (printf "\n~a\n" (make-string 60 #\=))
    (printf "~aOverall Summary:~a\n" BLUE RESET)
    (printf "  ~aCorrect:~a      ~a\n" GREEN RESET all-total-correct)
    (printf "  ~aIncorrect:~a    ~a\n" RED RESET all-total-incorrect)
    (printf "  ~aFailed:~a       ~a\n" RED RESET all-total-failed)
    (printf "  ~aMissing:~a      ~a\n" YELLOW RESET all-total-missing)
    (printf "  ~aTotal Verified:~a ~a\n" BLUE RESET all-total-verified))

  ;; Exit with appropriate status
  (cond
    [(or (> all-total-incorrect 0) (> all-total-failed 0))
     (exit 1)]
    [(> all-total-verified 0)
     (printf "\n~aAll verified solutions are correct!~a\n" GREEN RESET)]
    [else
     (printf "\n~aNo solutions were verified.~a\n" YELLOW RESET)]))

;; Parse command-line arguments and run verification
(define year-arg #f)
(define day-arg #f)
(define write-missing? #f)

(command-line
 #:program "verify_solutions.rkt"
 #:once-each
 [("-y" "--year") year
                  "Year to verify (e.g., 2015)"
                  (set! year-arg (string->number year))]
 [("-d" "--day") day
                 "Day to verify (1-25)"
                 (set! day-arg (string->number day))]
 [("-w" "--write-missing")
  "Write solution output to missing answer files"
  (set! write-missing? #t)]
 #:args args
 ;; Handle positional arguments
 (when (and (not (null? args)) (not year-arg))
   (set! year-arg (string->number (first args)))
   (set! args (rest args)))
 (when (and (not (null? args)) (not day-arg))
   (set! day-arg (string->number (first args)))))

;; Run the verification
(verify-solutions year-arg day-arg write-missing?)
