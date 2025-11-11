package main

// Advent of Code 2015 - Day 18: Like a GIF For Your Yard
// https://adventofcode.com/2015/day/18
//
// Game of Life variant with Christmas lights.
// After 100 steps, count how many lights are on.

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

	return newGrid
}

func (g Grid) countOn() int {
	return len(g)
}

func solvePart1(lines []string) int {
	grid := make(Grid)
	size := len(lines)

	for x, line := range lines {
		for y, ch := range line {
			if ch == '#' {
				grid[[2]int{x, y}] = true
			}
		}
	}

	for i := 0; i < 100; i++ {
		grid = grid.step(size)
	}

	return grid.countOn()
}

func main() {
	inputPath := input.GetInputPath(2015, 18)
	lines := input.MustReadLines(inputPath)

	answer := solvePart1(lines)
	utils.PrintSolution(1, answer)
}
