package main

// Advent of Code 2015 - Day 18, Part 2
// https://adventofcode.com/2015/day/18
//
// Same as Part 1, but the four corner lights are always on.

import (
	"github.com/dneff/adventofcode/go/pkg/input"
	"github.com/dneff/adventofcode/go/pkg/utils"
)

type Grid map[[2]int]bool

func (g Grid) countNeighbors(x, y int) int {
	count := 0
	for dx := -1; dx <= 1; dx++ {
		for dy := -1; dy <= 1; dy++ {
			if dx == 0 && dy == 0 {
				continue
			}
			if g[[2]int{x + dx, y + dy}] {
				count++
			}
		}
	}
	return count
}

func (g Grid) step(size int) Grid {
	newGrid := make(Grid)

	for x := 0; x < size; x++ {
		for y := 0; y < size; y++ {
			neighbors := g.countNeighbors(x, y)
			isOn := g[[2]int{x, y}]

			if isOn && (neighbors == 2 || neighbors == 3) {
				newGrid[[2]int{x, y}] = true
			} else if !isOn && neighbors == 3 {
				newGrid[[2]int{x, y}] = true
			}
		}
	}

	// Keep corners on
	newGrid[[2]int{0, 0}] = true
	newGrid[[2]int{0, size - 1}] = true
	newGrid[[2]int{size - 1, 0}] = true
	newGrid[[2]int{size - 1, size - 1}] = true

	return newGrid
}

func (g Grid) countOn() int {
	return len(g)
}

func solvePart2(lines []string) int {
	grid := make(Grid)
	size := len(lines)

	for x, line := range lines {
		for y, ch := range line {
			if ch == '#' {
				grid[[2]int{x, y}] = true
			}
		}
	}

	// Turn on corners initially
	grid[[2]int{0, 0}] = true
	grid[[2]int{0, size - 1}] = true
	grid[[2]int{size - 1, 0}] = true
	grid[[2]int{size - 1, size - 1}] = true

	for i := 0; i < 100; i++ {
		grid = grid.step(size)
	}

	return grid.countOn()
}

func main() {
	inputPath := input.GetInputPath(2015, 18)
	lines := input.MustReadLines(inputPath)

	answer := solvePart2(lines)
	utils.PrintSolution(2, answer)
}
