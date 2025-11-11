#ifndef AOC_MATH_H
#define AOC_MATH_H

#include <stddef.h>
#include <stdbool.h>

/**
 * Calculate the greatest common divisor (GCD) of two numbers.
 * @param a First number
 * @param b Second number
 * @return GCD of a and b
 */
long long gcd(long long a, long long b);

/**
 * Calculate the least common multiple (LCM) of two numbers.
 * @param a First number
 * @param b Second number
 * @return LCM of a and b
 */
long long lcm(long long a, long long b);

/**
 * Calculate the GCD of an array of numbers.
 * @param numbers Array of numbers
 * @param count Number of elements
 * @return GCD of all numbers
 */
long long gcd_array(const long long *numbers, size_t count);

/**
 * Calculate the LCM of an array of numbers.
 * @param numbers Array of numbers
 * @param count Number of elements
 * @return LCM of all numbers
 */
long long lcm_array(const long long *numbers, size_t count);

/**
 * Check if a number is prime.
 * @param n The number to check
 * @return true if prime, false otherwise
 */
bool is_prime(long long n);

/**
 * Calculate factorial.
 * @param n The number
 * @return n!
 */
long long factorial(int n);

/**
 * Calculate binomial coefficient (n choose k).
 * @param n The total number of items
 * @param k The number of items to choose
 * @return C(n, k)
 */
long long binomial(int n, int k);

/**
 * Calculate power (a^b) using fast exponentiation.
 * @param a Base
 * @param b Exponent
 * @return a^b
 */
long long power(long long a, int b);

/**
 * Calculate modular power ((a^b) % mod) using fast exponentiation.
 * @param a Base
 * @param b Exponent
 * @param mod Modulus
 * @return (a^b) % mod
 */
long long mod_power(long long a, long long b, long long mod);

/**
 * Get all prime numbers up to n using Sieve of Eratosthenes.
 * @param n Upper limit
 * @param count Pointer to store the count of primes
 * @return Array of prime numbers
 * @note Caller must free the returned array
 */
int *primes_up_to(int n, size_t *count);

/**
 * Get the prime factors of a number.
 * @param n The number to factor
 * @param count Pointer to store the count of factors
 * @return Array of prime factors (with repetition)
 * @note Caller must free the returned array
 */
long long *prime_factors(long long n, size_t *count);

/**
 * Get all divisors of a number.
 * @param n The number
 * @param count Pointer to store the count of divisors
 * @return Array of divisors
 * @note Caller must free the returned array
 */
long long *divisors(long long n, size_t *count);

#endif /* AOC_MATH_H */
