package main

// Advent of Code 2015 - Day 25: Let It Snow
// https://adventofcode.com/2015/day/25
//
// Generate codes in a diagonal pattern and find the code at a specific position.

import (
	"github.com/dneff/adventofcode/go/pkg/input"
	"github.com/dneff/adventofcode/go/pkg/utils"
)

func nextCode(current int) int {
	return (current * 252533) % 33554393
}

func getIterations(row, col int) int {
	maxRow := row + col - 1
	iterations := (maxRow * (maxRow - 1)) / 2
	iterations += col
	return iterations
}

func solvePart1(lines []string) int {
	nums := input.ParseInts(lines[0])
	row, col := nums[0], nums[1]

	code := 20151125
	iterations := getIterations(row, col)

	for i := 1; i < iterations; i++ {
		code = nextCode(code)
	}

	return code
}

func main() {
	inputPath := input.GetInputPath(2015, 25)
	lines := input.MustReadLines(inputPath)

	answer := solvePart1(lines)
	utils.PrintSolution(1, answer)
}
