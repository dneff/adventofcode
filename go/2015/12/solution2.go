package main

// Advent of Code 2015 - Day 12, Part 2
// https://adventofcode.com/2015/day/12
//
// Sum all numbers in a JSON document, ignoring any object
// (and all of its children) that has "red" as a value.

import (
	"encoding/json"
	"strings"

	"github.com/dneff/adventofcode/go/pkg/input"
	"github.com/dneff/adventofcode/go/pkg/utils"
)

func hasRedValue(obj map[string]interface{}) bool {
	for _, val := range obj {
		if str, ok := val.(string); ok && str == "red" {
			return true
		}
	}
	return false
}

func sumNumbersNoRed(data interface{}) int {
	sum := 0

	switch v := data.(type) {
	case float64:
		sum += int(v)
	case []interface{}:
		for _, item := range v {
			sum += sumNumbersNoRed(item)
		}
	case map[string]interface{}:
		if !hasRedValue(v) {
			for _, val := range v {
				sum += sumNumbersNoRed(val)
			}
		}
	}

	return sum
}

func solvePart2(jsonStr string) int {
	var data interface{}
	json.Unmarshal([]byte(jsonStr), &data)
	return sumNumbersNoRed(data)
}

func main() {
	inputPath := input.GetInputPath(2015, 12)
	content := input.MustReadFile(inputPath)
	content = strings.TrimSpace(content)

	answer := solvePart2(content)
	utils.PrintSolution(2, answer)
}
