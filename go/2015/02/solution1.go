package main

// Advent of Code 2015 - Day 2: I Was Told There Would Be No Math
// https://adventofcode.com/2015/day/2
//
// Calculate the total wrapping paper needed for presents.
// Each present is a rectangular prism with dimensions l x w x h.
// Wrapping paper needed = 2*l*w + 2*w*h + 2*h*l + area of smallest side.

import (
	"github.com/dneff/adventofcode/go/pkg/input"
	"github.com/dneff/adventofcode/go/pkg/math"
	"github.com/dneff/adventofcode/go/pkg/utils"
)

func getWrappingPaper(l, w, h int) int {
	sides := []int{l * w, w * h, h * l}
	wrapping := 2 * math.Sum(sides)
	slack := math.MinSlice(sides)
	return wrapping + slack
}

func solvePart1(lines []string) int {
	totalWrapping := 0
	for _, line := range lines {
		nums := input.ParseInts(line)
		if len(nums) == 3 {
			totalWrapping += getWrappingPaper(nums[0], nums[1], nums[2])
		}
	}
	return totalWrapping
}

func main() {
	inputPath := input.GetInputPath(2015, 2)
	lines := input.MustReadLines(inputPath)

	answer := solvePart1(lines)
	utils.PrintSolution(1, answer)
}
