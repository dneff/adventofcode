package main

// Advent of Code 2015 - Day 16: Aunt Sue
// https://adventofcode.com/2015/day/16
//
// Find which Aunt Sue sent you a gift by matching
// the detected compounds.

import (
	"strconv"
	"strings"

	"github.com/dneff/adventofcode/go/pkg/input"
	"github.com/dneff/adventofcode/go/pkg/utils"
)

func solvePart1(lines []string) int {
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
			if detected[key] == value {
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

	answer := solvePart1(lines)
	utils.PrintSolution(1, answer)
}
