package main

// Advent of Code 2015 - Day 11: Corporate Policy
// https://adventofcode.com/2015/day/11
//
// Find the next valid password. Password rules:
// 1. Must include one increasing straight of at least three letters (abc, bcd, etc.)
// 2. Must not contain i, o, or l
// 3. Must contain at least two different, non-overlapping pairs of letters

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
			i += 2 // Skip past this pair
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

func solvePart1(start string) string {
	return nextPassword(start)
}

func main() {
	inputPath := input.GetInputPath(2015, 11)
	content := input.MustReadFile(inputPath)
	content = strings.TrimSpace(content)

	answer := solvePart1(content)
	utils.PrintSolution(1, answer)
}
