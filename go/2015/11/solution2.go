package main

// Advent of Code 2015 - Day 11, Part 2
// https://adventofcode.com/2015/day/11
//
// Find the next valid password after the one from Part 1.

import (
	"strings"

	"github.com/dneff/adventofcode/go/pkg/input"
	"github.com/dneff/adventofcode/go/pkg/utils"
)

func hasStraight(s string) bool {
	for i := 0; i < len(s)-2; i++ {
		if s[i]+1 == s[i+1] && s[i]+2 == s[i+2] {
			return true
		}
	}
	return false
}

func hasInvalidChars(s string) bool {
	return strings.ContainsAny(s, "iol")
}

func hasTwoPairs(s string) bool {
	pairs := 0
	i := 0
	for i < len(s)-1 {
		if s[i] == s[i+1] {
			pairs++
			i += 2
			if pairs >= 2 {
				return true
			}
		} else {
			i++
		}
	}
	return false
}

func isValid(s string) bool {
	return hasStraight(s) && !hasInvalidChars(s) && hasTwoPairs(s)
}

func increment(s string) string {
	b := []byte(s)
	for i := len(b) - 1; i >= 0; i-- {
		if b[i] == 'z' {
			b[i] = 'a'
		} else {
			b[i]++
			break
		}
	}
	return string(b)
}

func nextPassword(current string) string {
	candidate := increment(current)
	for !isValid(candidate) {
		candidate = increment(candidate)
	}
	return candidate
}

func solvePart2(start string) string {
	first := nextPassword(start)
	return nextPassword(first)
}

func main() {
	inputPath := input.GetInputPath(2015, 11)
	content := input.MustReadFile(inputPath)
	content = strings.TrimSpace(content)

	answer := solvePart2(content)
	utils.PrintSolution(2, answer)
}
