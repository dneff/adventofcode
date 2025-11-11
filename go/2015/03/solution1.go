package main

// Advent of Code 2015 - Day 3: Perfectly Spherical Houses in a Vacuum
// https://adventofcode.com/2015/day/3
//
// Santa delivers presents to houses on an infinite 2D grid.
// Directions: ^ = north, v = south, > = east, < = west
// Count how many houses receive at least one present.

import (
	"strings"

	"github.com/dneff/adventofcode/go/pkg/input"
	"github.com/dneff/adventofcode/go/pkg/point"
	"github.com/dneff/adventofcode/go/pkg/utils"
)

func solvePart1(directions string) int {
	houses := make(map[point.Point]int)
	location := point.New(0, 0)
	houses[location]++

	for _, dir := range directions {
		switch dir {
		case '^':
			location = location.Add(point.North)
		case 'v':
			location = location.Add(point.South)
		case '>':
			location = location.Add(point.East)
		case '<':
			location = location.Add(point.West)
		}
		houses[location]++
	}

	return len(houses)
}

func main() {
	inputPath := input.GetInputPath(2015, 3)
	content := input.MustReadFile(inputPath)
	content = strings.TrimSpace(content)

	answer := solvePart1(content)
	utils.PrintSolution(1, answer)
}
