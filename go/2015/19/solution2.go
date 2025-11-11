package main

// Advent of Code 2015 - Day 19, Part 2
// https://adventofcode.com/2015/day/19
//
// Find the minimum number of steps to go from "e" to the target molecule.
// Use greedy approach: repeatedly apply longest matching replacement in reverse.

import (
	"strings"

	"github.com/dneff/adventofcode/go/pkg/input"
	"github.com/dneff/adventofcode/go/pkg/utils"
)

func solvePart2(lines []string) int {
	var replacements [][2]string
	var target string

	for _, line := range lines {
		line = strings.TrimSpace(line)
		if line == "" {
			continue
		}
		if strings.Contains(line, "=>") {
			parts := strings.Split(line, " => ")
			// Store in reverse (to => from) for backward search
			replacements = append(replacements, [2]string{parts[1], parts[0]})
		} else {
			target = line
		}
	}

	molecule := target
	steps := 0

	for molecule != "e" {
		for _, repl := range replacements {
			from, to := repl[0], repl[1]
			if strings.Contains(molecule, from) {
				molecule = strings.Replace(molecule, from, to, 1)
				steps++
				break
			}
		}
	}

	return steps
}

func main() {
	inputPath := input.GetInputPath(2015, 19)
	lines := input.MustReadLines(inputPath)

	answer := solvePart2(lines)
	utils.PrintSolution(2, answer)
}
