package main

// Advent of Code 2015 - Day 21, Part 2
// https://adventofcode.com/2015/day/21
//
// Find the maximum cost where you still lose the fight.

import (
	"github.com/dneff/adventofcode/go/pkg/input"
	"github.com/dneff/adventofcode/go/pkg/math"
	"github.com/dneff/adventofcode/go/pkg/utils"
)

type Item struct {
	cost, damage, armor int
}

var weapons = []Item{
	{8, 4, 0}, {10, 5, 0}, {25, 6, 0}, {40, 7, 0}, {74, 8, 0},
}

var armors = []Item{
	{0, 0, 0}, {13, 0, 1}, {31, 0, 2}, {53, 0, 3}, {75, 0, 4}, {102, 0, 5},
}

var rings = []Item{
	{0, 0, 0}, {25, 1, 0}, {50, 2, 0}, {100, 3, 0}, {20, 0, 1}, {40, 0, 2}, {80, 0, 3},
}

func playerWins(playerDamage, playerArmor, bossHP, bossDamage, bossArmor int) bool {
	playerHP := 100
	for {
		bossHP -= math.Max(1, playerDamage-bossArmor)
		if bossHP <= 0 {
			return true
		}
		playerHP -= math.Max(1, bossDamage-playerArmor)
		if playerHP <= 0 {
			return false
		}
	}
}

func solvePart2(lines []string) int {
	bossHP := input.ParseInts(lines[0])[0]
	bossDamage := input.ParseInts(lines[1])[0]
	bossArmor := input.ParseInts(lines[2])[0]

	maxCost := 0

	for _, weapon := range weapons {
		for _, armor := range armors {
			for i, ring1 := range rings {
				for j, ring2 := range rings {
					if i == j && i != 0 {
						continue
					}

					cost := weapon.cost + armor.cost + ring1.cost + ring2.cost
					damage := weapon.damage + armor.damage + ring1.damage + ring2.damage
					armorVal := weapon.armor + armor.armor + ring1.armor + ring2.armor

					if !playerWins(damage, armorVal, bossHP, bossDamage, bossArmor) {
						maxCost = math.Max(maxCost, cost)
					}
				}
			}
		}
	}

	return maxCost
}

func main() {
	inputPath := input.GetInputPath(2015, 21)
	lines := input.MustReadLines(inputPath)

	answer := solvePart2(lines)
	utils.PrintSolution(2, answer)
}
