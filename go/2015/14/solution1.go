package main

// Advent of Code 2015 - Day 14: Reindeer Olympics
// https://adventofcode.com/2015/day/14
//
// Calculate which reindeer travels the farthest after 2503 seconds.

import (
	"strings"

	"github.com/dneff/adventofcode/go/pkg/input"
	"github.com/dneff/adventofcode/go/pkg/math"
	"github.com/dneff/adventofcode/go/pkg/utils"
)

type Reindeer struct {
	speed    int
	flyTime  int
	restTime int
}

func (r *Reindeer) distanceAt(seconds int) int {
	cycleTime := r.flyTime + r.restTime
	fullCycles := seconds / cycleTime
	remainder := seconds % cycleTime

	distance := fullCycles * r.speed * r.flyTime

	if remainder >= r.flyTime {
		distance += r.speed * r.flyTime
	} else {
		distance += r.speed * remainder
	}

	return distance
}

func solvePart1(lines []string) int {
	raceTime := 2503
	maxDistance := 0

	for _, line := range lines {
		nums := input.ParseInts(line)
		if len(nums) >= 3 {
			reindeer := Reindeer{
				speed:    nums[0],
				flyTime:  nums[1],
				restTime: nums[2],
			}
			distance := reindeer.distanceAt(raceTime)
			maxDistance = math.Max(maxDistance, distance)
		}
	}

	return maxDistance
}

func main() {
	inputPath := input.GetInputPath(2015, 14)
	lines := input.MustReadLines(inputPath)

	answer := solvePart1(lines)
	utils.PrintSolution(1, answer)
}
