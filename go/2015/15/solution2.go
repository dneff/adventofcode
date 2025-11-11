package main

// Advent of Code 2015 - Day 15, Part 2
// https://adventofcode.com/2015/day/15
//
// Same as Part 1, but the recipe must have exactly 500 calories.

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

func calories(ingredients []Ingredient, amounts []int) int {
	total := 0
	for i, ing := range ingredients {
		total += ing.calories * amounts[i]
	}
	return total
}

func solvePart2(lines []string) int {
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
	targetCalories := 500

	for i1 := 0; i1 <= maxAmount; i1++ {
		for i2 := 0; i2 <= maxAmount-i1; i2++ {
			for i3 := 0; i3 <= maxAmount-i1-i2; i3++ {
				i4 := maxAmount - i1 - i2 - i3
				amounts := []int{i1, i2, i3, i4}

				if calories(ingredients, amounts) == targetCalories {
					score := scoreRecipe(ingredients, amounts)
					maxScore = math.Max(maxScore, score)
				}
			}
		}
	}

	return maxScore
}

func main() {
	inputPath := input.GetInputPath(2015, 15)
	lines := input.MustReadLines(inputPath)

	answer := solvePart2(lines)
	utils.PrintSolution(2, answer)
}
