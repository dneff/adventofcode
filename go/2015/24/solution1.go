package main

// Advent of Code 2015 - Day 24: It Hangs in the Balance
// https://adventofcode.com/2015/day/24
//
// Divide packages into 3 groups of equal weight. The first group
// should have the fewest packages. Find the quantum entanglement
// (product of package weights) of the ideal first group.

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

func solvePart1(lines []string) int {
	var packages []int
	for _, line := range lines {
		packages = append(packages, input.ParseInt(line))
	}

	totalWeight := math.Sum(packages)
	targetWeight := totalWeight / 3

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

	answer := solvePart1(lines)
	utils.PrintSolution(1, answer)
}
