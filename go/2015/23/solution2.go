package main

// Advent of Code 2015 - Day 23, Part 2
// https://adventofcode.com/2015/day/23
//
// Same as Part 1, but register a starts with value 1.

import (
	"strconv"
	"strings"

	"github.com/dneff/adventofcode/go/pkg/input"
	"github.com/dneff/adventofcode/go/pkg/utils"
)

type Computer struct {
	registers map[string]int
	pc        int
	program   [][]string
}

func NewComputer() *Computer {
	return &Computer{
		registers: map[string]int{"a": 1, "b": 0},
		pc:        0,
		program:   make([][]string, 0),
	}
}

func (c *Computer) load(lines []string) {
	for _, line := range lines {
		line = strings.TrimSpace(line)
		line = strings.ReplaceAll(line, ",", "")
		c.program = append(c.program, strings.Fields(line))
	}
}

func (c *Computer) run() {
	for c.pc < len(c.program) {
		inst := c.program[c.pc]
		switch inst[0] {
		case "hlf":
			c.registers[inst[1]] /= 2
			c.pc++
		case "tpl":
			c.registers[inst[1]] *= 3
			c.pc++
		case "inc":
			c.registers[inst[1]]++
			c.pc++
		case "jmp":
			offset, _ := strconv.Atoi(inst[1])
			c.pc += offset
		case "jie":
			if c.registers[inst[1]]%2 == 0 {
				offset, _ := strconv.Atoi(inst[2])
				c.pc += offset
			} else {
				c.pc++
			}
		case "jio":
			if c.registers[inst[1]] == 1 {
				offset, _ := strconv.Atoi(inst[2])
				c.pc += offset
			} else {
				c.pc++
			}
		}
	}
}

func solvePart2(lines []string) int {
	computer := NewComputer()
	computer.load(lines)
	computer.run()
	return computer.registers["b"]
}

func main() {
	inputPath := input.GetInputPath(2015, 23)
	lines := input.MustReadLines(inputPath)

	answer := solvePart2(lines)
	utils.PrintSolution(2, answer)
}
