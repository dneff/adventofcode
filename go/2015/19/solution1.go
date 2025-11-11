package main

// Advent of Code 2015 - Day 19: Medicine for Rudolph
// https://adventofcode.com/2015/day/19
//
// Count how many distinct molecules can be created by doing exactly one
// replacement on the starting molecule.

import (
	"strings"

	"github.com/dneff/adventofcode/go/pkg/input"
	"github.com/dneff/adventofcode/go/pkg/utils"
)

func solvePart1(lines []string) int {
	replacements := make(map[string][]string)
	var molecule string

	for _, line := range lines {
		line = strings.TrimSpace(line)
		if line == "" {
			continue
		}
		if strings.Contains(line, "=>") {
			parts := strings.Split(line, " => ")
			from, to := parts[0], parts[1]
			replacements[from] = append(replacements[from], to)
		} else {
			molecule = line
		}
	}

	distinctMolecules := make(map[string]bool)

	for from, toList := range replacements {
		// Find all occurrences of 'from' in the molecule
		for i := 0; i <= len(molecule)-len(from); i++ {
			if molecule[i:i+len(from)] == from {
				// Try each replacement
				for _, to := range toList {
					newMolecule := molecule[:i] + to + molecule[i+len(from):]
					distinctMolecules[newMolecule] = true
				}
			}
		}
	}

	return len(distinctMolecules)
}

func main() {
	inputPath := input.GetInputPath(2015, 19)
	lines := input.MustReadLines(inputPath)

	answer := solvePart1(lines)
	utils.PrintSolution(1, answer)
}
