package main

// Advent of Code 2015 - Day 2, Part 2
// https://adventofcode.com/2015/day/2
//
// Calculate the total ribbon needed for presents.
// Ribbon needed = smallest perimeter + bow (volume of box).

import (
	"github.com/dneff/adventofcode/go/pkg/input"
	"github.com/dneff/adventofcode/go/pkg/math"
	"github.com/dneff/adventofcode/go/pkg/utils"
)

func getRibbon(l, w, h int) int {
	perimeters := []int{l + w, w + h, h + l}
	ribbon := 2 * math.MinSlice(perimeters)
	return ribbon
}

func getBow(l, w, h int) int {
	return l * w * h
}

func solvePart2(lines []string) int {
	totalRibbon := 0
	for _, line := range lines {
		nums := input.ParseInts(line)
		if len(nums) == 3 {
			l, w, h := nums[0], nums[1], nums[2]
			totalRibbon += getRibbon(l, w, h) + getBow(l, w, h)
		}
	}
	return totalRibbon
}

func main() {
	inputPath := input.GetInputPath(2015, 2)
	lines := input.MustReadLines(inputPath)

	answer := solvePart2(lines)
	utils.PrintSolution(2, answer)
}
