package main

// Advent of Code 2015 - Day 17: No Such Thing as Too Much
// https://adventofcode.com/2015/day/17
//
// Find how many combinations of containers can exactly hold 150 liters of eggnog.

import (
	"github.com/dneff/adventofcode/go/pkg/input"
	"github.com/dneff/adventofcode/go/pkg/utils"
)

func solvePart1(lines []string) int {
	var containers []int
	for _, line := range lines {
		containers = append(containers, input.ParseInt(line))
	}

	target := 150
	validCombos := 0

	// Try all combinations using bitmask
	for i := 1; i < (1 << len(containers)); i++ {
		sum := 0
		for j := 0; j < len(containers); j++ {
			if i&(1<<j) != 0 {
				sum += containers[j]
			}
		}
		if sum == target {
			validCombos++
		}
	}

	return validCombos
}

func main() {
	inputPath := input.GetInputPath(2015, 17)
	lines := input.MustReadLines(inputPath)

	answer := solvePart1(lines)
	utils.PrintSolution(1, answer)
}
