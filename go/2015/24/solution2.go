package main

// Advent of Code 2015 - Day 24, Part 2
// https://adventofcode.com/2015/day/24
//
// Same as Part 1, but divide into 4 groups instead of 3.

import (
	"github.com/dneff/adventofcode/go/pkg/input"
	"github.com/dneff/adventofcode/go/pkg/math"
	"github.com/dneff/adventofcode/go/pkg/utils"
)

func combinations(arr []int, size int) [][]int {
	var result [][]int
	var helper func([]int, int, int)
	helper = func(combo []int, start, remaining int) {
		if remaining == 0 {
			tmp := make([]int, len(combo))
			copy(tmp, combo)
			result = append(result, tmp)
			return
		}
		for i := start; i < len(arr); i++ {
			helper(append(combo, arr[i]), i+1, remaining-1)
		}
	}
	helper([]int{}, 0, size)
	return result
}

func solvePart2(lines []string) int {
	var packages []int
	for _, line := range lines {
		packages = append(packages, input.ParseInt(line))
	}

	totalWeight := math.Sum(packages)
	targetWeight := totalWeight / 4

	// Find minimum group size and lowest quantum entanglement
	for groupSize := 1; groupSize <= len(packages); groupSize++ {
		minQE := -1

		for _, combo := range combinations(packages, groupSize) {
			if math.Sum(combo) == targetWeight {
				qe := math.Product(combo)
				if minQE == -1 || qe < minQE {
					minQE = qe
				}
			}
		}

		if minQE != -1 {
			return minQE
		}
	}

	return -1
}

func main() {
	inputPath := input.GetInputPath(2015, 24)
	lines := input.MustReadLines(inputPath)

	answer := solvePart2(lines)
	utils.PrintSolution(2, answer)
}
