package main

// Advent of Code 2015 - Day 7: Some Assembly Required
// https://adventofcode.com/2015/day/7
//
// Simulate a circuit of wires and bitwise logic gates.
// Each wire carries a 16-bit signal (0-65535).
// Operations: AND, OR, LSHIFT, RSHIFT, NOT
// Goal: Determine the signal on wire 'a'.

import (
	"strconv"
	"strings"

	"github.com/dneff/adventofcode/go/pkg/input"
	"github.com/dneff/adventofcode/go/pkg/utils"
)

type Circuit struct {
	wires map[string]uint16
}

func NewCircuit() *Circuit {
	return &Circuit{wires: make(map[string]uint16)}
}

func (c *Circuit) getValue(s string) (uint16, bool) {
	// Try to parse as number
	if val, err := strconv.ParseUint(s, 10, 16); err == nil {
		return uint16(val), true
	}
	// Otherwise it's a wire name
	val, ok := c.wires[s]
	return val, ok
}

func (c *Circuit) processInstruction(instruction string) bool {
	parts := strings.Split(instruction, " -> ")
	dest := parts[1]

	// Skip if already computed
	if _, exists := c.wires[dest]; exists {
		return true
	}

	source := strings.Fields(parts[0])

	if len(source) == 1 {
		// Direct assignment
		if val, ok := c.getValue(source[0]); ok {
			c.wires[dest] = val
			return true
		}
	} else if len(source) == 2 {
		// NOT operation
		if val, ok := c.getValue(source[1]); ok {
			c.wires[dest] = ^val
			return true
		}
	} else if len(source) == 3 {
		// Binary operations
		left, right := source[0], source[2]
		op := source[1]

		leftVal, leftOk := c.getValue(left)
		rightVal, rightOk := c.getValue(right)

		if leftOk && rightOk {
			switch op {
			case "AND":
				c.wires[dest] = leftVal & rightVal
			case "OR":
				c.wires[dest] = leftVal | rightVal
			case "LSHIFT":
				c.wires[dest] = leftVal << rightVal
			case "RSHIFT":
				c.wires[dest] = leftVal >> rightVal
			}
			return true
		}
	}

	return false
}

func solvePart1(lines []string) uint16 {
	circuit := NewCircuit()
	pending := make([]string, 0)

	for _, line := range lines {
		pending = append(pending, strings.TrimSpace(line))
	}

	for len(pending) > 0 {
		newPending := make([]string, 0)
		for _, instruction := range pending {
			if !circuit.processInstruction(instruction) {
				newPending = append(newPending, instruction)
			}
		}
		pending = newPending
	}

	return circuit.wires["a"]
}

func main() {
	inputPath := input.GetInputPath(2015, 7)
	lines := input.MustReadLines(inputPath)

	answer := solvePart1(lines)
	utils.PrintSolution(1, answer)
}
