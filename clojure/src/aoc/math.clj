(ns aoc.math
  "Mathematical utilities for Advent of Code."
  (:require [clojure.math.combinatorics :as combo]))

(defn gcd
  "Calculate the greatest common divisor of two numbers.

   Parameters:
   - a: First number
   - b: Second number

   Returns: GCD of a and b"
  [a b]
  (if (zero? b)
    a
    (recur b (mod a b))))

(defn lcm
  "Calculate the least common multiple of two numbers.

   Parameters:
   - a: First number
   - b: Second number

   Returns: LCM of a and b"
  [a b]
  (/ (* a b) (gcd a b)))

(defn lcm-of
  "Calculate the least common multiple of a sequence of numbers.

   Parameters:
   - nums: Sequence of numbers

   Returns: LCM of all numbers"
  [nums]
  (reduce lcm nums))

(defn factorial
  "Calculate the factorial of n.

   Parameters:
   - n: Non-negative integer

   Returns: n!"
  [n]
  (reduce *' (range 1 (inc n))))

(defn is-prime?
  "Check if a number is prime.

   Parameters:
   - n: Integer to test

   Returns: Boolean"
  [n]
  (cond
    (< n 2) false
    (= n 2) true
    (even? n) false
    :else (not-any? #(zero? (mod n %))
                    (range 3 (inc (Math/sqrt n)) 2))))

(defn primes-up-to
  "Generate all prime numbers up to n using Sieve of Eratosthenes.

   Parameters:
   - n: Upper limit (inclusive)

   Returns: Sequence of primes"
  [n]
  (if (< n 2)
    []
    (let [sieve (boolean-array (inc n) true)]
      (aset sieve 0 false)
      (aset sieve 1 false)
      (doseq [i (range 2 (inc (Math/sqrt n)))
              :when (aget sieve i)]
        (doseq [j (range (* i i) (inc n) i)]
          (aset sieve j false)))
      (filter #(aget sieve %) (range 2 (inc n))))))

(defn prime-factors
  "Get the prime factorization of n.

   Parameters:
   - n: Positive integer

   Returns: Sequence of prime factors (with duplicates)"
  [n]
  (loop [n n
         d 2
         factors []]
    (cond
      (<= n 1) factors
      (zero? (mod n d)) (recur (/ n d) d (conj factors d))
      :else (recur n (inc d) factors))))

(defn divisors
  "Get all divisors of n.

   Parameters:
   - n: Positive integer

   Returns: Sequence of divisors"
  [n]
  (filter #(zero? (mod n %)) (range 1 (inc n))))

(defn permutations
  "Generate all permutations of a collection.

   Parameters:
   - coll: Collection to permute

   Returns: Sequence of permutations"
  [coll]
  (combo/permutations coll))

(defn combinations
  "Generate all k-combinations of a collection.

   Parameters:
   - coll: Collection
   - k: Size of combinations

   Returns: Sequence of combinations"
  [coll k]
  (combo/combinations coll k))

(defn cartesian-product
  "Generate the Cartesian product of collections.

   Parameters:
   - & colls: Variable number of collections

   Returns: Sequence of tuples"
  [& colls]
  (combo/cartesian-product colls))

(defn pow
  "Calculate base^exp.

   Parameters:
   - base: Base number
   - exp: Exponent (integer)

   Returns: base^exp"
  [base exp]
  (reduce *' (repeat exp base)))

(defn abs
  "Absolute value of a number.

   Parameters:
   - n: Number

   Returns: |n|"
  [n]
  (Math/abs n))

(defn sign
  "Get the sign of a number.

   Parameters:
   - n: Number

   Returns: 1 for positive, -1 for negative, 0 for zero"
  [n]
  (cond
    (pos? n) 1
    (neg? n) -1
    :else 0))

(defn sum
  "Sum a sequence of numbers.

   Parameters:
   - nums: Sequence of numbers

   Returns: Sum"
  [nums]
  (reduce + 0 nums))

(defn product
  "Product of a sequence of numbers.

   Parameters:
   - nums: Sequence of numbers

   Returns: Product"
  [nums]
  (reduce * 1 nums))

(defn median
  "Calculate the median of a sequence of numbers.

   Parameters:
   - nums: Sequence of numbers

   Returns: Median value"
  [nums]
  (let [sorted (sort nums)
        n (count sorted)
        mid (quot n 2)]
    (if (odd? n)
      (nth sorted mid)
      (/ (+ (nth sorted mid) (nth sorted (dec mid))) 2))))

(defn mean
  "Calculate the mean of a sequence of numbers.

   Parameters:
   - nums: Sequence of numbers

   Returns: Mean value"
  [nums]
  (/ (sum nums) (count nums)))

(defn mod-pow
  "Calculate (base^exp) mod m efficiently.

   Parameters:
   - base: Base number
   - exp: Exponent
   - m: Modulus

   Returns: (base^exp) mod m"
  [base exp m]
  (loop [result 1
         base (mod base m)
         exp exp]
    (cond
      (zero? exp) result
      (odd? exp) (recur (mod (* result base) m) base (dec exp))
      :else (recur result (mod (* base base) m) (quot exp 2)))))

(defn digits
  "Get the digits of a number.

   Parameters:
   - n: Non-negative integer

   Returns: Sequence of digits"
  [n]
  (if (zero? n)
    [0]
    (loop [n n
           result []]
      (if (zero? n)
        (reverse result)
        (recur (quot n 10) (conj result (mod n 10)))))))

(defn from-digits
  "Construct a number from a sequence of digits.

   Parameters:
   - digits: Sequence of digits

   Returns: Integer"
  [digits]
  (reduce (fn [acc d] (+ (* acc 10) d)) 0 digits))
