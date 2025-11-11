package main

// Advent of Code 2015 - Day 3, Part 2
// https://adventofcode.com/2015/day/3
//
// Santa and Robo-Santa take turns delivering presents.
// Santa follows odd-indexed directions, Robo-Santa follows even-indexed.
// Count how many houses receive at least one present.

import (
	"strings"

	"github.com/dneff/adventofcode/go/pkg/input"
	"github.com/dneff/adventofcode/go/pkg/point"
	"github.com/dneff/adventofcode/go/pkg/utils"
)

func solvePart2(directions string) int {
	houses := make(map[point.Point]int)
	santaLocation := point.New(0, 0)
	roboLocation := point.New(0, 0)

	houses[santaLocation]++

	for i, dir := range directions {
		var location *point.Point
		if i%2 == 0 {
			location = &santaLocation
		} else {
			location = &roboLocation
		}

		switch dir {
		case '^':
			*location = location.Add(point.North)
		case 'v':
			*location = location.Add(point.South)
		case '>':
			*location = location.Add(point.East)
		case '<':
			*location = location.Add(point.West)
		}
		houses[*location]++
	}

	return len(houses)
}

func main() {
	inputPath := input.GetInputPath(2015, 3)
	content := input.MustReadFile(inputPath)
	content = strings.TrimSpace(content)

	answer := solvePart2(content)
	utils.PrintSolution(2, answer)
}
