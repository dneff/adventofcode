package main

// Advent of Code 2015 - Day 8, Part 2
// https://adventofcode.com/2015/day/8
//
// Encode the strings by escaping special characters and adding quotes.
// Calculate the difference between encoded length and original length.

import (
	"strings"

	"github.com/dneff/adventofcode/go/pkg/input"
	"github.com/dneff/adventofcode/go/pkg/utils"
)

func encodeString(s string) string {
	// Escape backslashes and quotes
	s = strings.ReplaceAll(s, "\\", "\\\\")
	s = strings.ReplaceAll(s, "\"", "\\\"")
	// Add surrounding quotes
	return "\"" + s + "\""
}

func solvePart2(lines []string) int {
	totalOriginal := 0
	totalEncoded := 0

	for _, line := range lines {
		line = strings.TrimSpace(line)
		if line == "" {
			continue
		}
		totalOriginal += len(line)
		encoded := encodeString(line)
		totalEncoded += len(encoded)
	}

	return totalEncoded - totalOriginal
}

func main() {
	inputPath := input.GetInputPath(2015, 8)
	lines := input.MustReadLines(inputPath)

	answer := solvePart2(lines)
	utils.PrintSolution(2, answer)
}
