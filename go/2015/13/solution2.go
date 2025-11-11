package main

// Advent of Code 2015 - Day 13, Part 2
// https://adventofcode.com/2015/day/13
//
// Add yourself to the seating arrangement with 0 happiness
// change for all neighbors.

import (
	"strings"

	"github.com/dneff/adventofcode/go/pkg/input"
	"github.com/dneff/adventofcode/go/pkg/utils"
)

func parseHappiness(lines []string) (map[string]map[string]int, []string) {
	happiness := make(map[string]map[string]int)
	people := make([]string, 0)

	for _, line := range lines {
		line = strings.TrimSpace(line)
		line = strings.TrimSuffix(line, ".")
		line = strings.Replace(line, "would gain ", "", 1)
		line = strings.Replace(line, "would lose ", "-", 1)

		parts := strings.Fields(line)
		person := parts[0]
		neighbor := parts[len(parts)-1]
		value := input.ParseInt(parts[1])

		if _, exists := happiness[person]; !exists {
			happiness[person] = make(map[string]int)
			people = append(people, person)
		}
		happiness[person][neighbor] = value
	}

	return happiness, people
}

func calculateHappiness(arrangement []string, happiness map[string]map[string]int) int {
	total := 0
	n := len(arrangement)

	for i := 0; i < n; i++ {
		left := arrangement[(i-1+n)%n]
		right := arrangement[(i+1)%n]
		person := arrangement[i]

		total += happiness[person][left]
		total += happiness[person][right]
	}

	return total
}

func solvePart2(lines []string) int {
	happiness, people := parseHappiness(lines)

	// Add yourself with 0 happiness for all neighbors
	myself := "me"
	happiness[myself] = make(map[string]int)
	for _, person := range people {
		happiness[myself][person] = 0
		happiness[person][myself] = 0
	}
	people = append(people, myself)

	arrangements := utils.Permute(people)
	maxHappiness := 0

	for _, arrangement := range arrangements {
		h := calculateHappiness(arrangement, happiness)
		if h > maxHappiness {
			maxHappiness = h
		}
	}

	return maxHappiness
}

func main() {
	inputPath := input.GetInputPath(2015, 13)
	lines := input.MustReadLines(inputPath)

	answer := solvePart2(lines)
	utils.PrintSolution(2, answer)
}
