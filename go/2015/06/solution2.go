package main

// Advent of Code 2015 - Day 6, Part 2
// https://adventofcode.com/2015/day/6
//
// Control a 1000x1000 grid of lights with brightness levels.
// "turn on" increases brightness by 1
// "turn off" decreases brightness by 1 (minimum 0)
// "toggle" increases brightness by 2
// Calculate total brightness.

import (
	"strings"

	"github.com/dneff/adventofcode/go/pkg/input"
	"github.com/dneff/adventofcode/go/pkg/math"
	"github.com/dneff/adventofcode/go/pkg/utils"
)

type BrightnessLights struct {
	grid map[[2]int]int
}

func NewBrightnessLights() *BrightnessLights {
	return &BrightnessLights{grid: make(map[[2]int]int)}
}

func (l *BrightnessLights) turnOn(x1, y1, x2, y2 int) {
	for x := x1; x <= x2; x++ {
		for y := y1; y <= y2; y++ {
			l.grid[[2]int{x, y}]++
		}
	}
}

func (l *BrightnessLights) turnOff(x1, y1, x2, y2 int) {
	for x := x1; x <= x2; x++ {
		for y := y1; y <= y2; y++ {
			key := [2]int{x, y}
			l.grid[key] = math.Max(0, l.grid[key]-1)
		}
	}
}

func (l *BrightnessLights) toggle(x1, y1, x2, y2 int) {
	for x := x1; x <= x2; x++ {
		for y := y1; y <= y2; y++ {
			l.grid[[2]int{x, y}] += 2
		}
	}
}

func (l *BrightnessLights) totalBrightness() int {
	total := 0
	for _, brightness := range l.grid {
		total += brightness
	}
	return total
}

func solvePart2(lines []string) int {
	lights := NewBrightnessLights()

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

	return lights.totalBrightness()
}

func main() {
	inputPath := input.GetInputPath(2015, 6)
	lines := input.MustReadLines(inputPath)

	answer := solvePart2(lines)
	utils.PrintSolution(2, answer)
}
