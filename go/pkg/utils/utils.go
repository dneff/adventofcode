// Package utils provides common utility functions for Advent of Code solutions.
package utils

import (
	"fmt"
	"strings"
)

// PrintSolution prints the solution in a consistent format.
func PrintSolution(part int, answer interface{}) {
	fmt.Printf("Part %d: %v\n", part, answer)
}

// Check panics if an error is non-nil.
// Useful for competitive programming where errors should fail fast.
func Check(err error) {
	if err != nil {
		panic(err)
	}
}

// Must1 returns the first value and panics if the error is non-nil.
// Useful for chaining operations: val := Must1(someFunc())
func Must1[T any](val T, err error) T {
	Check(err)
	return val
}

// Must panics if the error is non-nil.
// Useful when you only care about the error: Must(someFunc())
func Must(err error) {
	Check(err)
}

// CountIf counts elements in a slice that match a predicate.
func CountIf[T any](slice []T, predicate func(T) bool) int {
	count := 0
	for _, item := range slice {
		if predicate(item) {
			count++
		}
	}
	return count
}

// Filter returns a new slice containing only elements that match the predicate.
func Filter[T any](slice []T, predicate func(T) bool) []T {
	var result []T
	for _, item := range slice {
		if predicate(item) {
			result = append(result, item)
		}
	}
	return result
}

// Map applies a function to each element and returns a new slice.
func Map[T, U any](slice []T, fn func(T) U) []U {
	result := make([]U, len(slice))
	for i, item := range slice {
		result[i] = fn(item)
	}
	return result
}

// Reduce reduces a slice to a single value using a function.
func Reduce[T, U any](slice []T, initial U, fn func(U, T) U) U {
	result := initial
	for _, item := range slice {
		result = fn(result, item)
	}
	return result
}

// All returns true if all elements match the predicate.
func All[T any](slice []T, predicate func(T) bool) bool {
	for _, item := range slice {
		if !predicate(item) {
			return false
		}
	}
	return true
}

// Any returns true if any element matches the predicate.
func Any[T any](slice []T, predicate func(T) bool) bool {
	for _, item := range slice {
		if predicate(item) {
			return true
		}
	}
	return false
}

// Contains checks if a slice contains a value.
func Contains[T comparable](slice []T, value T) bool {
	for _, item := range slice {
		if item == value {
			return true
		}
	}
	return false
}

// Index returns the index of the first occurrence of value, or -1 if not found.
func Index[T comparable](slice []T, value T) int {
	for i, item := range slice {
		if item == value {
			return i
		}
	}
	return -1
}

// Reverse returns a new slice with elements in reverse order.
func Reverse[T any](slice []T) []T {
	result := make([]T, len(slice))
	for i, item := range slice {
		result[len(slice)-1-i] = item
	}
	return result
}

// ReverseInPlace reverses a slice in place.
func ReverseInPlace[T any](slice []T) {
	for i, j := 0, len(slice)-1; i < j; i, j = i+1, j-1 {
		slice[i], slice[j] = slice[j], slice[i]
	}
}

// Unique returns a new slice with duplicate elements removed (preserves order).
func Unique[T comparable](slice []T) []T {
	seen := make(map[T]bool)
	var result []T
	for _, item := range slice {
		if !seen[item] {
			seen[item] = true
			result = append(result, item)
		}
	}
	return result
}

// Frequencies returns a map counting occurrences of each element.
func Frequencies[T comparable](slice []T) map[T]int {
	freq := make(map[T]int)
	for _, item := range slice {
		freq[item]++
	}
	return freq
}

// GroupBy groups elements by a key function.
func GroupBy[T any, K comparable](slice []T, keyFn func(T) K) map[K][]T {
	groups := make(map[K][]T)
	for _, item := range slice {
		key := keyFn(item)
		groups[key] = append(groups[key], item)
	}
	return groups
}

// Chunk splits a slice into chunks of specified size.
func Chunk[T any](slice []T, size int) [][]T {
	var chunks [][]T
	for i := 0; i < len(slice); i += size {
		end := i + size
		if end > len(slice) {
			end = len(slice)
		}
		chunks = append(chunks, slice[i:end])
	}
	return chunks
}

// Flatten flattens a 2D slice into a 1D slice.
func Flatten[T any](slices [][]T) []T {
	var result []T
	for _, slice := range slices {
		result = append(result, slice...)
	}
	return result
}

// Zip combines two slices into a slice of pairs.
// The result length is the minimum of the two input lengths.
func Zip[T, U any](a []T, b []U) [][2]interface{} {
	length := len(a)
	if len(b) < length {
		length = len(b)
	}
	result := make([][2]interface{}, length)
	for i := 0; i < length; i++ {
		result[i] = [2]interface{}{a[i], b[i]}
	}
	return result
}

// Permute generates all permutations of a slice.
func Permute[T any](slice []T) [][]T {
	var result [][]T
	var helper func([]T, int)
	helper = func(arr []T, n int) {
		if n == 1 {
			tmp := make([]T, len(arr))
			copy(tmp, arr)
			result = append(result, tmp)
		} else {
			for i := 0; i < n; i++ {
				helper(arr, n-1)
				if n%2 == 1 {
					arr[0], arr[n-1] = arr[n-1], arr[0]
				} else {
					arr[i], arr[n-1] = arr[n-1], arr[i]
				}
			}
		}
	}
	helper(slice, len(slice))
	return result
}

// SetFromSlice creates a set (map[T]bool) from a slice.
func SetFromSlice[T comparable](slice []T) map[T]bool {
	set := make(map[T]bool)
	for _, item := range slice {
		set[item] = true
	}
	return set
}

// SetUnion returns the union of two sets.
func SetUnion[T comparable](a, b map[T]bool) map[T]bool {
	result := make(map[T]bool)
	for k := range a {
		result[k] = true
	}
	for k := range b {
		result[k] = true
	}
	return result
}

// SetIntersection returns the intersection of two sets.
func SetIntersection[T comparable](a, b map[T]bool) map[T]bool {
	result := make(map[T]bool)
	for k := range a {
		if b[k] {
			result[k] = true
		}
	}
	return result
}

// SetDifference returns elements in a that are not in b.
func SetDifference[T comparable](a, b map[T]bool) map[T]bool {
	result := make(map[T]bool)
	for k := range a {
		if !b[k] {
			result[k] = true
		}
	}
	return result
}

// SplitAny splits a string by any of the given separators.
func SplitAny(s string, seps string) []string {
	return strings.FieldsFunc(s, func(r rune) bool {
		return strings.ContainsRune(seps, r)
	})
}

// Transpose transposes a 2D slice (swaps rows and columns).
func Transpose[T any](matrix [][]T) [][]T {
	if len(matrix) == 0 {
		return [][]T{}
	}
	rows := len(matrix)
	cols := len(matrix[0])
	result := make([][]T, cols)
	for i := range result {
		result[i] = make([]T, rows)
		for j := range result[i] {
			result[i][j] = matrix[j][i]
		}
	}
	return result
}

// Memoize creates a memoized version of a function with one argument.
func Memoize[K comparable, V any](fn func(K) V) func(K) V {
	cache := make(map[K]V)
	return func(key K) V {
		if val, ok := cache[key]; ok {
			return val
		}
		val := fn(key)
		cache[key] = val
		return val
	}
}
