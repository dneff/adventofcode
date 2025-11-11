package main

// Advent of Code 2015 - Day 20: Infinite Elves and Infinite Houses
// https://adventofcode.com/2015/day/20
//
// Find the lowest house number that receives at least the target number of presents.
// Each elf N delivers 10 presents to every Nth house.

import (
	"strings"

	"github.com/dneff/adventofcode/go/pkg/input"
	"github.com/dneff/adventofcode/go/pkg/utils"
)

func solvePart1(target int) int {
	maxHouse := target / 10
	presents := make([]int, maxHouse+1)

	for elf := 1; elf <= maxHouse; elf++ {
		for house := elf; house <= maxHouse; house += elf {
			presents[house] += 10 * elf
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

	answer := solvePart1(target)
	utils.PrintSolution(1, answer)
}
