package main

// Advent of Code 2015 - Day 6: Probably a Fire Hazard
// https://adventofcode.com/2015/day/6
//
// Control a 1000x1000 grid of lights using instructions.
// Instructions: "turn on", "turn off", "toggle"
// Count how many lights are lit at the end.

import (
	"strings"

	"github.com/dneff/adventofcode/go/pkg/input"
	"github.com/dneff/adventofcode/go/pkg/utils"
)

type Lights struct {
	grid map[[2]int]bool
}

func NewLights() *Lights {
	return &Lights{grid: make(map[[2]int]bool)}
}

func (l *Lights) turnOn(x1, y1, x2, y2 int) {
	for x := x1; x <= x2; x++ {
		for y := y1; y <= y2; y++ {
			l.grid[[2]int{x, y}] = true
		}
	}
}

func (l *Lights) turnOff(x1, y1, x2, y2 int) {
	for x := x1; x <= x2; x++ {
		for y := y1; y <= y2; y++ {
			l.grid[[2]int{x, y}] = false
		}
	}
}

func (l *Lights) toggle(x1, y1, x2, y2 int) {
	for x := x1; x <= x2; x++ {
		for y := y1; y <= y2; y++ {
			key := [2]int{x, y}
			l.grid[key] = !l.grid[key]
		}
	}
}

func (l *Lights) countLit() int {
	count := 0
	for _, lit := range l.grid {
		if lit {
			count++
		}
	}
	return count
}

func solvePart1(lines []string) int {
	lights := NewLights()

	for _, line := range lines {
		line = strings.TrimSpace(line)
		line = strings.Replace(line, "turn on", "on", 1)
		line = strings.Replace(line, "turn off", "off", 1)
		line = strings.Replace(line, "through", "", 1)

		parts := strings.Fields(line)
		action := parts[0]
		coords1 := input.ParseInts(parts[1])
		coords2 := input.ParseInts(parts[2])

		x1, y1 := coords1[0], coords1[1]
		x2, y2 := coords2[0], coords2[1]

		switch action {
		case "on":
			lights.turnOn(x1, y1, x2, y2)
		case "off":
			lights.turnOff(x1, y1, x2, y2)
		case "toggle":
			lights.toggle(x1, y1, x2, y2)
		}
	}

	return lights.countLit()
}

func main() {
	inputPath := input.GetInputPath(2015, 6)
	lines := input.MustReadLines(inputPath)

	answer := solvePart1(lines)
	utils.PrintSolution(1, answer)
}
