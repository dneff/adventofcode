package main

// Advent of Code 2015 - Day 5, Part 2
// https://adventofcode.com/2015/day/5
//
// Determine if strings are "nice" based on two new rules:
// 1. Contains a pair of letters that appears at least twice without overlapping
// 2. Contains a letter that repeats with exactly one letter between them

import (
	"strings"

	"github.com/dneff/adventofcode/go/pkg/input"
	"github.com/dneff/adventofcode/go/pkg/utils"
)

func hasPairTwice(s string) bool {
	for i := 1; i < len(s); i++ {
		pair := s[i-1 : i+1]
		// Check if pair appears before or after current position
		if strings.Contains(s[:i-1], pair) || strings.Contains(s[i+1:], pair) {
			return true
		}
	}
	return false
}

func hasRepeatWithGap(s string) bool {
	for i := 2; i < len(s); i++ {
		if s[i] == s[i-2] {
			return true
		}
	}
	return false
}

func isNice2(s string) bool {
	return hasPairTwice(s) && hasRepeatWithGap(s)
}

func solvePart2(lines []string) int {
	count := 0
	for _, line := range lines {
		if isNice2(strings.TrimSpace(line)) {
			count++
		}
	}
	return count
}

func main() {
	inputPath := input.GetInputPath(2015, 5)
	lines := input.MustReadLines(inputPath)

	answer := solvePart2(lines)
	utils.PrintSolution(2, answer)
}
