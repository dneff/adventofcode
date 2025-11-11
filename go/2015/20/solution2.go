package main

// Advent of Code 2015 - Day 20, Part 2
// https://adventofcode.com/2015/day/20
//
// Each elf delivers 11 presents but only visits 50 houses.

import (
	"strings"

	"github.com/dneff/adventofcode/go/pkg/input"
	"github.com/dneff/adventofcode/go/pkg/utils"
)

func solvePart2(target int) int {
	maxHouse := target / 10
	presents := make([]int, maxHouse+1)

	for elf := 1; elf <= maxHouse; elf++ {
		delivered := 0
		for house := elf; house <= maxHouse && delivered < 50; house += elf {
			presents[house] += 11 * elf
			delivered++
		}
	}

	for house := 1; house <= maxHouse; house++ {
		if presents[house] >= target {
			return house
		}
	}

	return -1
}

func main() {
	inputPath := input.GetInputPath(2015, 20)
	content := input.MustReadFile(inputPath)
	target := input.ParseInt(strings.TrimSpace(content))

	answer := solvePart2(target)
	utils.PrintSolution(2, answer)
}
