package main

// Advent of Code 2015 - Day 8: Matchsticks
// https://adventofcode.com/2015/day/8
//
// Calculate the difference between the number of characters in the code
// representation of string literals and the number of characters in memory.

import (
	"strconv"
	"strings"

	"github.com/dneff/adventofcode/go/pkg/input"
	"github.com/dneff/adventofcode/go/pkg/utils"
)

func countMemoryChars(s string) int {
	// Remove surrounding quotes
	s = s[1 : len(s)-1]

	count := 0
	i := 0
	for i < len(s) {
		if s[i] == '\\' {
			if i+1 < len(s) {
				if s[i+1] == '\\' || s[i+1] == '"' {
					count++
					i += 2
				} else if s[i+1] == 'x' && i+3 < len(s) {
					// Hex escape sequence
					count++
					i += 4
				} else {
					count++
					i++
				}
			} else {
				count++
				i++
			}
		} else {
			count++
			i++
		}
	}

	return count
}

func solvePart1(lines []string) int {
	totalCode := 0
	totalMemory := 0

	for _, line := range lines {
		line = strings.TrimSpace(line)
		if line == "" {
			continue
		}
		totalCode += len(line)
		totalMemory += countMemoryChars(line)
	}

	return totalCode - totalMemory
}

func main() {
	inputPath := input.GetInputPath(2015, 8)
	lines := input.MustReadLines(inputPath)

	answer := solvePart1(lines)
	utils.PrintSolution(1, answer)
}
