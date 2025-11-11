package main

// Advent of Code 2015 - Day 1: Not Quite Lisp
// https://adventofcode.com/2015/day/1
//
// This script calculates the final floor Santa ends up on after following
// the instructions in the input file. Each '(' means go up one floor,
// each ')' means go down one floor.

import (
	"strings"

	"github.com/dneff/adventofcode/go/pkg/input"
	"github.com/dneff/adventofcode/go/pkg/utils"
)

func solvePart1(instructions string) int {
	floor := 0
	for _, ch := range instructions {
		if ch == '(' {
			floor++
		} else if ch == ')' {
			floor--
		}
	}
	return floor
}

func main() {
	inputPath := input.GetInputPath(2015, 1)
	content := input.MustReadFile(inputPath)
	content = strings.TrimSpace(content)

	answer := solvePart1(content)
	utils.PrintSolution(1, answer)
}
