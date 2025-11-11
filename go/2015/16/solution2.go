package main

// Advent of Code 2015 - Day 16, Part 2
// https://adventofcode.com/2015/day/16
//
// Find Aunt Sue with different matching rules:
// cats and trees: value must be GREATER than detected
// pomeranians and goldfish: value must be FEWER than detected

import (
	"strconv"
	"strings"

	"github.com/dneff/adventofcode/go/pkg/input"
	"github.com/dneff/adventofcode/go/pkg/utils"
)

func solvePart2(lines []string) int {
	detected := map[string]int{
		"children":    3,
		"cats":        7,
		"samoyeds":    2,
		"pomeranians": 3,
		"akitas":      0,
		"vizslas":     0,
		"goldfish":    5,
		"trees":       3,
		"cars":        2,
		"perfumes":    1,
	}

	aunts := make(map[int]map[string]int)
	matches := make(map[int]int)

	for _, line := range lines {
		line = strings.TrimSpace(line)
		line = strings.TrimPrefix(line, "Sue ")
		line = strings.ReplaceAll(line, ":", "")
		line = strings.ReplaceAll(line, ",", "")

		parts := strings.Fields(line)
		auntNum, _ := strconv.Atoi(parts[0])

		aunts[auntNum] = make(map[string]int)

		for i := 1; i < len(parts); i += 2 {
			if i+1 < len(parts) {
				key := parts[i]
				value, _ := strconv.Atoi(parts[i+1])
				aunts[auntNum][key] = value
			}
		}
	}

	for auntNum, details := range aunts {
		for key, value := range details {
			match := false
			if key == "cats" || key == "trees" {
				match = value > detected[key]
			} else if key == "pomeranians" || key == "goldfish" {
				match = value < detected[key]
			} else {
				match = value == detected[key]
			}

			if match {
				matches[auntNum]++
			}
		}
	}

	maxMatches := 0
	bestAunt := 0
	for aunt, count := range matches {
		if count > maxMatches {
			maxMatches = count
			bestAunt = aunt
		}
	}

	return bestAunt
}

func main() {
	inputPath := input.GetInputPath(2015, 16)
	lines := input.MustReadLines(inputPath)

	answer := solvePart2(lines)
	utils.PrintSolution(2, answer)
}
