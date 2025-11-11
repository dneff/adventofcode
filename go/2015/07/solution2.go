package main

// Advent of Code 2015 - Day 7, Part 2
// https://adventofcode.com/2015/day/7
//
// Same as Part 1, but override wire 'b' with the signal from wire 'a'
// from Part 1, then recalculate the signal on wire 'a'.

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
	if val, err := strconv.ParseUint(s, 10, 16); err == nil {
		return uint16(val), true
	}
	val, ok := c.wires[s]
	return val, ok
}

func (c *Circuit) processInstruction(instruction string) bool {
	parts := strings.Split(instruction, " -> ")
	dest := parts[1]

	if _, exists := c.wires[dest]; exists {
		return true
	}

	source := strings.Fields(parts[0])

	if len(source) == 1 {
		if val, ok := c.getValue(source[0]); ok {
			c.wires[dest] = val
			return true
		}
	} else if len(source) == 2 {
		if val, ok := c.getValue(source[1]); ok {
			c.wires[dest] = ^val
			return true
		}
	} else if len(source) == 3 {
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

func runCircuit(lines []string, overrideB uint16) uint16 {
	circuit := NewCircuit()
	circuit.wires["b"] = overrideB
	pending := make([]string, 0)

	for _, line := range lines {
		line = strings.TrimSpace(line)
		// Skip the original instruction for wire 'b'
		if strings.HasSuffix(line, "-> b") {
			continue
		}
		pending = append(pending, line)
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

func solvePart2(lines []string) uint16 {
	// First, run part 1 to get the value for wire 'a'
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

	valueA := circuit.wires["a"]

	// Now run again with wire 'b' overridden
	return runCircuit(lines, valueA)
}

func main() {
	inputPath := input.GetInputPath(2015, 7)
	lines := input.MustReadLines(inputPath)

	answer := solvePart2(lines)
	utils.PrintSolution(2, answer)
}
