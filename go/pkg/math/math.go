// Package math provides mathematical utilities for Advent of Code problems.
package math

import (
	"math"
)

// Abs returns the absolute value of x.
func Abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

// Abs64 returns the absolute value of x.
func Abs64(x int64) int64 {
	if x < 0 {
		return -x
	}
	return x
}

// Min returns the minimum of two integers.
func Min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

// Max returns the maximum of two integers.
func Max(a, b int) int {
	if a > b {
		return a
	}
	return b
}

// Min64 returns the minimum of two int64 values.
func Min64(a, b int64) int64 {
	if a < b {
		return a
	}
	return b
}

// Max64 returns the maximum of two int64 values.
func Max64(a, b int64) int64 {
	if a > b {
		return a
	}
	return b
}

// MinSlice returns the minimum value in a slice.
func MinSlice(nums []int) int {
	if len(nums) == 0 {
		panic("MinSlice: empty slice")
	}
	min := nums[0]
	for _, n := range nums[1:] {
		if n < min {
			min = n
		}
	}
	return min
}

// MaxSlice returns the maximum value in a slice.
func MaxSlice(nums []int) int {
	if len(nums) == 0 {
		panic("MaxSlice: empty slice")
	}
	max := nums[0]
	for _, n := range nums[1:] {
		if n > max {
			max = n
		}
	}
	return max
}

// GCD returns the greatest common divisor of a and b.
func GCD(a, b int) int {
	for b != 0 {
		a, b = b, a%b
	}
	return a
}

// GCD64 returns the greatest common divisor of a and b.
func GCD64(a, b int64) int64 {
	for b != 0 {
		a, b = b, a%b
	}
	return a
}

// LCM returns the least common multiple of a and b.
func LCM(a, b int) int {
	return a * b / GCD(a, b)
}

// LCM64 returns the least common multiple of a and b.
func LCM64(a, b int64) int64 {
	return a * b / GCD64(a, b)
}

// LCMSlice returns the LCM of all numbers in a slice.
func LCMSlice(nums []int) int {
	if len(nums) == 0 {
		return 0
	}
	result := nums[0]
	for _, n := range nums[1:] {
		result = LCM(result, n)
	}
	return result
}

// IsPrime checks if a number is prime using trial division.
func IsPrime(n int) bool {
	if n < 2 {
		return false
	}
	if n == 2 {
		return true
	}
	if n%2 == 0 {
		return false
	}
	sqrt := int(math.Sqrt(float64(n)))
	for i := 3; i <= sqrt; i += 2 {
		if n%i == 0 {
			return false
		}
	}
	return true
}

// PrimesUpTo returns all prime numbers up to n using the Sieve of Eratosthenes.
func PrimesUpTo(n int) []int {
	if n < 2 {
		return []int{}
	}

	// Create a boolean array and initialize all entries as true
	isPrime := make([]bool, n+1)
	for i := range isPrime {
		isPrime[i] = true
	}

	for p := 2; p*p <= n; p++ {
		if isPrime[p] {
			// Mark all multiples of p as not prime
			for i := p * p; i <= n; i += p {
				isPrime[i] = false
			}
		}
	}

	// Collect all prime numbers
	var primes []int
	for p := 2; p <= n; p++ {
		if isPrime[p] {
			primes = append(primes, p)
		}
	}

	return primes
}

// Factorial returns n! (n factorial).
func Factorial(n int) int {
	if n < 0 {
		panic("factorial: negative number")
	}
	if n == 0 || n == 1 {
		return 1
	}
	result := 1
	for i := 2; i <= n; i++ {
		result *= i
	}
	return result
}

// Pow returns base^exp using fast exponentiation.
func Pow(base, exp int) int {
	result := 1
	for exp > 0 {
		if exp%2 == 1 {
			result *= base
		}
		base *= base
		exp /= 2
	}
	return result
}

// PowMod returns (base^exp) % mod using fast modular exponentiation.
func PowMod(base, exp, mod int) int {
	result := 1
	base %= mod
	for exp > 0 {
		if exp%2 == 1 {
			result = (result * base) % mod
		}
		base = (base * base) % mod
		exp /= 2
	}
	return result
}

// Sum returns the sum of all integers in a slice.
func Sum(nums []int) int {
	sum := 0
	for _, n := range nums {
		sum += n
	}
	return sum
}

// Sum64 returns the sum of all int64 values in a slice.
func Sum64(nums []int64) int64 {
	var sum int64
	for _, n := range nums {
		sum += n
	}
	return sum
}

// Product returns the product of all integers in a slice.
func Product(nums []int) int {
	if len(nums) == 0 {
		return 0
	}
	product := 1
	for _, n := range nums {
		product *= n
	}
	return product
}

// Combinations returns the binomial coefficient C(n, k) = n! / (k! * (n-k)!)
func Combinations(n, k int) int {
	if k > n || k < 0 {
		return 0
	}
	if k == 0 || k == n {
		return 1
	}
	// Optimize by using C(n, k) = C(n, n-k)
	if k > n-k {
		k = n - k
	}
	result := 1
	for i := 0; i < k; i++ {
		result *= (n - i)
		result /= (i + 1)
	}
	return result
}

// Permutations returns the number of permutations P(n, k) = n! / (n-k)!
func Permutations(n, k int) int {
	if k > n || k < 0 {
		return 0
	}
	result := 1
	for i := 0; i < k; i++ {
		result *= (n - i)
	}
	return result
}

// Sign returns the sign of x: -1 if negative, 0 if zero, 1 if positive.
func Sign(x int) int {
	if x < 0 {
		return -1
	}
	if x > 0 {
		return 1
	}
	return 0
}
