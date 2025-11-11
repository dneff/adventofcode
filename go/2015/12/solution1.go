package main

// Advent of Code 2015 - Day 12: JSAbacusFramework.io
// https://adventofcode.com/2015/day/12
//
// Sum all numbers in a JSON document.

import (
	"encoding/json"
	"strings"

	"github.com/dneff/adventofcode/go/pkg/input"
	"github.com/dneff/adventofcode/go/pkg/utils"
)

func sumNumbers(data interface{}) int {
	sum := 0

	switch v := data.(type) {
	case float64:
		sum += int(v)
	case []interface{}:
		for _, item := range v {
			sum += sumNumbers(item)
		}
	case map[string]interface{}:
		for _, val := range v {
			sum += sumNumbers(val)
		}
	}

	return sum
}

func solvePart1(jsonStr string) int {
	var data interface{}
	json.Unmarshal([]byte(jsonStr), &data)
	return sumNumbers(data)
}

func main() {
	inputPath := input.GetInputPath(2015, 12)
	content := input.MustReadFile(inputPath)
	content = strings.TrimSpace(content)

	answer := solvePart1(content)
	utils.PrintSolution(1, answer)
}
