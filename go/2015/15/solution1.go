package main

// Advent of Code 2015 - Day 15: Science for Hungry People
// https://adventofcode.com/2015/day/15
//
// Find the optimal cookie recipe using 100 teaspoons of ingredients
// to maximize the total score (product of property scores).

import (
	"github.com/dneff/adventofcode/go/pkg/input"
	"github.com/dneff/adventofcode/go/pkg/math"
	"github.com/dneff/adventofcode/go/pkg/utils"
)

type Ingredient struct {
	capacity   int
	durability int
	flavor     int
	texture    int
	calories   int
}

func scoreRecipe(ingredients []Ingredient, amounts []int) int {
	capacity := 0
	durability := 0
	flavor := 0
	texture := 0

	for i, ing := range ingredients {
		capacity += ing.capacity * amounts[i]
		durability += ing.durability * amounts[i]
		flavor += ing.flavor * amounts[i]
		texture += ing.texture * amounts[i]
	}

	if capacity <= 0 || durability <= 0 || flavor <= 0 || texture <= 0 {
		return 0
	}

	return capacity * durability * flavor * texture
}

func solvePart1(lines []string) int {
	var ingredients []Ingredient

	for _, line := range lines {
		nums := input.ParseInts(line)
		if len(nums) >= 5 {
			ingredients = append(ingredients, Ingredient{
				capacity:   nums[0],
				durability: nums[1],
				flavor:     nums[2],
				texture:    nums[3],
				calories:   nums[4],
			})
		}
	}

	maxScore := 0
	maxAmount := 100

	// Assuming 4 ingredients based on the problem
	for i1 := 0; i1 <= maxAmount; i1++ {
		for i2 := 0; i2 <= maxAmount-i1; i2++ {
			for i3 := 0; i3 <= maxAmount-i1-i2; i3++ {
				i4 := maxAmount - i1 - i2 - i3
				amounts := []int{i1, i2, i3, i4}
				score := scoreRecipe(ingredients, amounts)
				maxScore = math.Max(maxScore, score)
			}
		}
	}

	return maxScore
}

func main() {
	inputPath := input.GetInputPath(2015, 15)
	lines := input.MustReadLines(inputPath)

	answer := solvePart1(lines)
	utils.PrintSolution(1, answer)
}
