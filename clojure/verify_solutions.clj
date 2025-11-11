#!/usr/bin/env bb
;;
;; Verify Advent of Code Clojure solutions against known correct answers.
;;
;; This script runs each solution namespace for a specified year and compares
;; the output against the answer files stored in aoc-data.
;;
;; Usage:
;;     clojure -M verify_solutions.clj [YEAR] [DAY] [OPTIONS]
;;     or
;;     ./verify_solutions.clj [YEAR] [DAY] [OPTIONS]
;;
;; Positional Arguments:
;;     YEAR                      The year to verify (e.g., 2015, 2016, 2017)
;;     DAY                       The day to verify (1-25)
;;
;; Options:
;;     --year YEAR, -y YEAR      The year to verify (alternative to positional)
;;     --day DAY, -d DAY         The day to verify (alternative to positional)
;;     --write-missing, -w       Write solution output to missing answer files
;;
;; Examples:
;;     clojure -M verify_solutions.clj              # Verify all years
;;     clojure -M verify_solutions.clj 2015         # Verify year 2015
;;     clojure -M verify_solutions.clj 2015 20      # Verify year 2015, day 20
;;     clojure -M verify_solutions.clj --year 2015 --day 20 --write-missing
;;
;; If no year is specified, all years will be verified.
;; If no day is specified, all days will be verified.

(require '[clojure.java.io :as io]
         '[clojure.string :as str]
         '[clojure.java.shell :as shell])

;; ANSI color codes
(def GREEN "\033[92m")
(def RED "\033[91m")
(def YELLOW "\033[93m")
(def BLUE "\033[94m")
(def RESET "\033[0m")

(defn get-time-emoji
  "Get an emoji based on execution time in seconds."
  [elapsed-time]
  (cond
    (< elapsed-time 1.0) "⚡"
    (< elapsed-time 3.0) "🚀"
    (< elapsed-time 10.0) "▶️"
    (< elapsed-time 30.0) "🐢"
    :else "🐌"))

(defn get-expected-answer
  "Read expected answer from aoc-data directory.
   Returns the expected answer as a string, or nil if not found."
  [day part year]
  (let [answer-file (io/file (str "../aoc-data/" year "/" day "/solution-" part))]
    (when (.exists answer-file)
      (try
        (let [content (str/trim (slurp answer-file))]
          (when (and (seq content) (not= content "0"))
            content))
        (catch Exception _ nil)))))

(defn write-answer
  "Write an answer to the aoc-data directory.
   Returns true if successfully written, false otherwise."
  [day part year answer]
  (let [answer-dir (io/file (str "../aoc-data/" year "/" day))
        answer-file (io/file answer-dir (str "solution-" part))]
    (try
      (.mkdirs answer-dir)
      (spit answer-file (str (str/trim answer) "\n"))
      true
      (catch Exception e
        (println (str RED "Error writing answer: " (.getMessage e) RESET))
        false))))

(defn run-solution
  "Run a solution namespace and extract the answer.
   Returns a map with :answer, :success, :elapsed-time, :file-exists"
  [day part year]
  (let [day-str (format "%02d" day)
        namespace-name (str "aoc.year" year ".day" day-str)
        solve-fn (str "solve-part" part)
        clj-file (io/file (str "src/aoc/year" year "/day" day-str ".clj"))]
    (if-not (.exists clj-file)
      {:answer nil :success false :elapsed-time 0.0 :file-exists false}
      (try
        (let [start-time (System/nanoTime)
              ;; Run the solution using clojure CLI
              result (shell/sh "clojure" "-M" "-e"
                              (str "(require '" namespace-name ") "
                                   "(println (str \"Part " part ": \" "
                                   "(" namespace-name "/" solve-fn ")))")
                              :dir (str (System/getProperty "user.dir")))
              elapsed-time (/ (- (System/nanoTime) start-time) 1e9)]
          (if (zero? (:exit result))
            ;; Extract answer from output
            (let [lines (str/split-lines (:out result))
                  part-line (some #(when (str/includes? % (str "Part " part ":")) %) lines)]
              (if part-line
                (let [answer (str/trim (last (str/split part-line #":")))]
                  {:answer answer :success true :elapsed-time elapsed-time :file-exists true})
                {:answer nil :success false :elapsed-time elapsed-time :file-exists true}))
            {:answer nil :success false :elapsed-time elapsed-time :file-exists true}))
        (catch Exception e
          {:answer nil :success false :elapsed-time 0.0 :file-exists true})))))

(defn get-years-to-verify
  "Get list of years to verify based on existing solution directories."
  [year-filter]
  (if year-filter
    [year-filter]
    (let [src-dir (io/file "src/aoc")]
      (if (.exists src-dir)
        (->> (.listFiles src-dir)
             (filter #(.isDirectory %))
             (map #(.getName %))
             (filter #(str/starts-with? % "year"))
             (map #(Integer/parseInt (subs % 4)))
             (sort)
             (vec))
        []))))

(defn parse-args
  "Parse command line arguments."
  [args]
  (loop [args args
         result {:year nil :day nil :write-missing false}]
    (if (empty? args)
      result
      (let [arg (first args)]
        (cond
          (or (= arg "--write-missing") (= arg "-w"))
          (recur (rest args) (assoc result :write-missing true))

          (or (= arg "--year") (= arg "-y"))
          (recur (drop 2 args) (assoc result :year (Integer/parseInt (second args))))

          (or (= arg "--day") (= arg "-d"))
          (recur (drop 2 args) (assoc result :day (Integer/parseInt (second args))))

          ;; Positional arguments
          (and (nil? (:year result)) (re-matches #"\d+" arg))
          (recur (rest args) (assoc result :year (Integer/parseInt arg)))

          (and (:year result) (nil? (:day result)) (re-matches #"\d+" arg))
          (recur (rest args) (assoc result :day (Integer/parseInt arg)))

          :else
          (recur (rest args) result))))))

(defn verify-solutions
  "Main verification logic."
  [args]
  (let [opts (parse-args args)
        years-to-verify (get-years-to-verify (:year opts))
        days-to-verify (if (:day opts)
                        [(:day opts)]
                        (range 1 26))]

    (when (empty? years-to-verify)
      (println (str RED "Error: No Clojure solution directories found" RESET))
      (System/exit 1))

    (when (and (:day opts) (or (< (:day opts) 1) (> (:day opts) 25)))
      (println (str RED "Error: Day must be between 1 and 25" RESET))
      (System/exit 1))

    ;; Track overall statistics
    (let [overall-stats (atom {:correct 0 :incorrect 0 :failed 0 :missing 0 :verified 0})]

      (doseq [year years-to-verify]
        (let [aoc-data-dir (io/file (str "../aoc-data/" year))]

          (when (and (not (.exists aoc-data-dir)) (not (:write-missing opts)))
            (println (str YELLOW "Warning: aoc-data directory not found for year " year RESET))
            (println (str "Expected directory: " (.getPath aoc-data-dir)))
            (println "Continuing anyway, but no answers will be verified."))

          (when (> (count years-to-verify) 1)
            (println (str "\n" BLUE "Verifying " year " Advent of Code Solutions" RESET))
            (println (apply str (repeat 60 "="))))
          (when (= (count years-to-verify) 1)
            (println (str BLUE "Verifying " year " Advent of Code Solutions" RESET))
            (println (apply str (repeat 60 "="))))

          (let [year-stats (atom {:correct 0 :incorrect 0 :failed 0 :missing 0 :verified 0 :written 0})]

            (doseq [day days-to-verify
                    part [1 2]]
              (let [expected (get-expected-answer day part year)
                    {:keys [answer success elapsed-time file-exists]} (run-solution day part year)]

                (cond
                  ;; Case 1: No solution file, no expected answer -> Skip
                  (and (not file-exists) (nil? expected))
                  nil

                  ;; Case 2: No solution file, but has expected answer
                  (and (not file-exists) expected)
                  (do
                    (println (format "%s○%s Day %2d Part %d: %sMISSING%s (solution file not found)"
                                    YELLOW RESET day part YELLOW RESET))
                    (swap! year-stats update :missing inc))

                  ;; Case 3: Solution file exists but failed to run
                  (and file-exists (or (not success) (nil? answer)))
                  (let [emoji (get-time-emoji elapsed-time)]
                    (println (format "%s✗%s Day %2d Part %d: %sFAILED TO RUN%s (%.3fs) %s"
                                    RED RESET day part RED RESET elapsed-time emoji))
                    (swap! year-stats update :failed inc))

                  ;; Case 4: Solution ran but no expected answer
                  (nil? expected)
                  (let [emoji (get-time-emoji elapsed-time)
                        status-msg (if (:write-missing opts)
                                    (if (write-answer day part year answer)
                                      (do
                                        (swap! year-stats update :written inc)
                                        (str YELLOW "MISSING (wrote: " answer ")" RESET))
                                      (str YELLOW "MISSING (failed to write)" RESET))
                                    (str YELLOW "MISSING" RESET))]
                    (println (format "%s○%s Day %2d Part %d: %s (answer: %s, %.3fs) %s"
                                    YELLOW RESET day part status-msg answer elapsed-time emoji))
                    (swap! year-stats update :missing inc))

                  ;; Case 5: Solution ran and has expected answer -> Compare
                  :else
                  (do
                    (swap! year-stats update :verified inc)
                    (if (= answer expected)
                      (let [emoji (get-time-emoji elapsed-time)]
                        (println (format "%s✓%s Day %2d Part %d: %sCORRECT%s (answer: %s, %.3fs) %s"
                                        GREEN RESET day part GREEN RESET answer elapsed-time emoji))
                        (swap! year-stats update :correct inc))
                      (let [emoji (get-time-emoji elapsed-time)]
                        (println (format "%s✗%s Day %2d Part %d: %sINCORRECT%s (expected: %s, got: %s, %.3fs) %s"
                                        RED RESET day part RED RESET expected answer elapsed-time emoji))
                        (swap! year-stats update :incorrect inc)))))))

            ;; Print year summary
            (let [stats @year-stats]
              (println (str "\n" (apply str (repeat 60 "="))))
              (println (str BLUE "Summary for " year ":" RESET))
              (println (str "  " GREEN "Correct:      " RESET (:correct stats)))
              (println (str "  " RED "Incorrect:    " RESET (:incorrect stats)))
              (println (str "  " RED "Failed:       " RESET (:failed stats)))
              (println (str "  " YELLOW "Missing:      " RESET (:missing stats)))
              (when (and (:write-missing opts) (> (:written stats) 0))
                (println (str "  " YELLOW "Written:      " RESET (:written stats))))
              (println (str "  " BLUE "Total Verified: " RESET (:verified stats)))

              ;; Update overall stats
              (swap! overall-stats update :correct + (:correct stats))
              (swap! overall-stats update :incorrect + (:incorrect stats))
              (swap! overall-stats update :failed + (:failed stats))
              (swap! overall-stats update :missing + (:missing stats))
              (swap! overall-stats update :verified + (:verified stats))))))

      ;; Print overall summary if multiple years
      (when (> (count years-to-verify) 1)
        (let [stats @overall-stats]
          (println (str "\n" (apply str (repeat 60 "="))))
          (println (str BLUE "Overall Summary:" RESET))
          (println (str "  " GREEN "Correct:      " RESET (:correct stats)))
          (println (str "  " RED "Incorrect:    " RESET (:incorrect stats)))
          (println (str "  " RED "Failed:       " RESET (:failed stats)))
          (println (str "  " YELLOW "Missing:      " RESET (:missing stats)))
          (println (str "  " BLUE "Total Verified: " RESET (:verified stats)))))

      ;; Exit with appropriate code
      (let [stats @overall-stats]
        (if (or (> (:incorrect stats) 0) (> (:failed stats) 0))
          (System/exit 1)
          (if (> (:verified stats) 0)
            (println (str "\n" GREEN "All verified solutions are correct!" RESET))
            (println (str "\n" YELLOW "No solutions were verified." RESET))))))))

;; Main entry point
(verify-solutions *command-line-args*)
