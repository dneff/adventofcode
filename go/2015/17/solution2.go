package main

// Advent of Code 2015 - Day 17, Part 2
// https://adventofcode.com/2015/day/17
//
// Find how many ways you can use the minimum number of containers
// to store exactly 150 liters.

import (
	"github.com/dneff/adventofcode/go/pkg/input"
	"github.com/dneff/adventofcode/go/pkg/math"
	"github.com/dneff/adventofcode/go/pkg/utils"
)

func countBits(n int) int {
	count := 0
	for n > 0 {
		count += n & 1
		n >>= 1
	}
	return count
}

func solvePart2(lines []string) int {
	var containers []int
	for _, line := range lines {
		containers = append(containers, input.ParseInt(line))
	}

	target := 150
	minContainers := len(containers) + 1
	validCombos := make(map[int]int)

	// Try all combinations using bitmask
	for i := 1; i < (1 << len(containers)); i++ {
		sum := 0
		numContainers := countBits(i)

		for j := 0; j < len(containers); j++ {
			if i&(1<<j) != 0 {
				sum += containers[j]
			}
		}

		if sum == target {
			validCombos[numContainers]++
			minContainers = math.Min(minContainers, numContainers)
		}
	}

	return validCombos[minContainers]
}

func main() {
	inputPath := input.GetInputPath(2015, 17)
	lines := input.MustReadLines(inputPath)

	answer := solvePart2(lines)
	utils.PrintSolution(2, answer)
}
