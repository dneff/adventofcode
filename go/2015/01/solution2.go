package main

// Advent of Code 2015 - Day 1, Part 2
// https://adventofcode.com/2015/day/1
//
// This script finds the position of the first character in the input that
// causes Santa to enter the basement (floor -1).

import (
	"strings"

	"github.com/dneff/adventofcode/go/pkg/input"
	"github.com/dneff/adventofcode/go/pkg/utils"
)

func findBasementEntry(instructions string) int {
	floor := 0
	for i, ch := range instructions {
		if ch == '(' {
			floor++
		} else if ch == ')' {
			floor--
		}
		if floor == -1 {
			return i + 1
		}
	}
	return -1
}

func main() {
	inputPath := input.GetInputPath(2015, 1)
	content := input.MustReadFile(inputPath)
	content = strings.TrimSpace(content)

	answer := findBasementEntry(content)
	utils.PrintSolution(2, answer)
}
