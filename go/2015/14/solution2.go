package main

// Advent of Code 2015 - Day 14, Part 2
// https://adventofcode.com/2015/day/14
//
// Award points to the leading reindeer(s) at each second.
// Winner is the reindeer with the most points after 2503 seconds.

import (
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

func solvePart2(lines []string) int {
	raceTime := 2503
	var reindeer []Reindeer

	for _, line := range lines {
		nums := input.ParseInts(line)
		if len(nums) >= 3 {
			reindeer = append(reindeer, Reindeer{
				speed:    nums[0],
				flyTime:  nums[1],
				restTime: nums[2],
			})
		}
	}

	points := make([]int, len(reindeer))

	for t := 1; t <= raceTime; t++ {
		distances := make([]int, len(reindeer))
		maxDist := 0

		for i, r := range reindeer {
			distances[i] = r.distanceAt(t)
			maxDist = math.Max(maxDist, distances[i])
		}

		for i, dist := range distances {
			if dist == maxDist {
				points[i]++
			}
		}
	}

	return math.MaxSlice(points)
}

func main() {
	inputPath := input.GetInputPath(2015, 14)
	lines := input.MustReadLines(inputPath)

	answer := solvePart2(lines)
	utils.PrintSolution(2, answer)
}
