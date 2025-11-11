package main

// Advent of Code 2015 - Day 5: Doesn't He Have Intern-Elves For This?
// https://adventofcode.com/2015/day/5
//
// Determine if strings are "nice" based on three rules:
// 1. Contains at least three vowels (aeiou)
// 2. Contains at least one letter that appears twice in a row
// 3. Does not contain the strings ab, cd, pq, or xy

import (
	"strings"

	"github.com/dneff/adventofcode/go/pkg/input"
	"github.com/dneff/adventofcode/go/pkg/utils"
)

func hasThreeVowels(s string) bool {
	vowels := "aeiou"
	count := 0
	for _, ch := range s {
		if strings.ContainsRune(vowels, ch) {
			count++
		}
	}
	return count >= 3
}

func hasDoubleLetter(s string) bool {
	for i := 1; i < len(s); i++ {
		if s[i] == s[i-1] {
			return true
		}
	}
	return false
}

func noForbiddenPairs(s string) bool {
	forbidden := []string{"ab", "cd", "pq", "xy"}
	for _, pair := range forbidden {
		if strings.Contains(s, pair) {
			return false
		}
	}
	return true
}

func isNice(s string) bool {
	return hasThreeVowels(s) && hasDoubleLetter(s) && noForbiddenPairs(s)
}

func solvePart1(lines []string) int {
	count := 0
	for _, line := range lines {
		if isNice(strings.TrimSpace(line)) {
			count++
		}
	}
	return count
}

func main() {
	inputPath := input.GetInputPath(2015, 5)
	lines := input.MustReadLines(inputPath)

	answer := solvePart1(lines)
	utils.PrintSolution(1, answer)
}
