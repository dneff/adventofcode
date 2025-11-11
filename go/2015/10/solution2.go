package main

// Advent of Code 2015 - Day 10, Part 2
// https://adventofcode.com/2015/day/10
//
// Same as Part 1, but apply the process 50 times.

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

func solvePart2(start string, iterations int) int {
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

	answer := solvePart2(content, 50)
	utils.PrintSolution(2, answer)
}
