package main

// Advent of Code 2015 - Day 10: Elves Look, Elves Say
// https://adventofcode.com/2015/day/10
//
// Implement the look-and-say sequence.
// Example: "1" becomes "11" (one 1), "11" becomes "21" (two 1s), etc.
// Apply this process 40 times and find the length.

import (
	"strconv"
	"strings"

	"github.com/dneff/adventofcode/go/pkg/input"
	"github.com/dneff/adventofcode/go/pkg/utils"
)

func lookAndSay(s string) string {
	if len(s) == 0 {
		return ""
	}

	var result strings.Builder
	count := 1
	current := s[0]

	for i := 1; i < len(s); i++ {
		if s[i] == current {
			count++
		} else {
			result.WriteString(strconv.Itoa(count))
			result.WriteByte(current)
			current = s[i]
			count = 1
		}
	}

	result.WriteString(strconv.Itoa(count))
	result.WriteByte(current)

	return result.String()
}

func solvePart1(start string, iterations int) int {
	sequence := start
	for i := 0; i < iterations; i++ {
		sequence = lookAndSay(sequence)
	}
	return len(sequence)
}

func main() {
	inputPath := input.GetInputPath(2015, 10)
	content := input.MustReadFile(inputPath)
	content = strings.TrimSpace(content)

	answer := solvePart1(content, 40)
	utils.PrintSolution(1, answer)
}
