package main

// Advent of Code 2015 - Day 22, Part 2
// https://adventofcode.com/2015/day/22
//
// Same as Part 1, but player loses 1 HP at the start of each player turn (hard mode).

import (
	"github.com/dneff/adventofcode/go/pkg/input"
	"github.com/dneff/adventofcode/go/pkg/math"
	"github.com/dneff/adventofcode/go/pkg/utils"
)

type Spell struct {
	name   string
	cost   int
	damage int
	heal   int
	armor  int
	mana   int
	turns  int
}

var spells = []Spell{
	{"missile", 53, 4, 0, 0, 0, 0},
	{"drain", 73, 2, 2, 0, 0, 0},
	{"shield", 113, 0, 0, 7, 0, 6},
	{"poison", 173, 3, 0, 0, 0, 6},
	{"recharge", 229, 0, 0, 0, 101, 5},
}

type State struct {
	playerHP   int
	playerMana int
	bossHP     int
	manaUsed   int
	effects    []Effect
}

type Effect struct {
	spell Spell
	turns int
}

func (s *State) copy() *State {
	newState := &State{
		playerHP:   s.playerHP,
		playerMana: s.playerMana,
		bossHP:     s.bossHP,
		manaUsed:   s.manaUsed,
		effects:    make([]Effect, len(s.effects)),
	}
	copy(newState.effects, s.effects)
	return newState
}

func (s *State) applyEffects() {
	newEffects := []Effect{}

	for _, eff := range s.effects {
		s.bossHP -= eff.spell.damage
		s.playerMana += eff.spell.mana
		eff.turns--
		if eff.turns > 0 {
			newEffects = append(newEffects, eff)
		}
	}

	s.effects = newEffects
}

func (s *State) hasEffect(spellName string) bool {
	for _, eff := range s.effects {
		if eff.spell.name == spellName {
			return true
		}
	}
	return false
}

var minMana = 1000000

func simulate(state *State, bossAttack int) {
	if state.manaUsed >= minMana {
		return
	}

	// Hard mode: player loses 1 HP at start of player turn
	state.playerHP--
	if state.playerHP <= 0 {
		return
	}

	// Player turn - apply effects
	state.applyEffects()
	if state.bossHP <= 0 {
		minMana = math.Min(minMana, state.manaUsed)
		return
	}

	// Try each spell
	for _, spell := range spells {
		if state.hasEffect(spell.name) || spell.cost > state.playerMana {
			continue
		}

		newState := state.copy()
		newState.playerMana -= spell.cost
		newState.manaUsed += spell.cost

		if spell.turns > 0 {
			newState.effects = append(newState.effects, Effect{spell, spell.turns})
		} else {
			newState.bossHP -= spell.damage
			newState.playerHP += spell.heal
		}

		if newState.bossHP <= 0 {
			minMana = math.Min(minMana, newState.manaUsed)
			continue
		}

		// Boss turn - apply effects
		newState.applyEffects()
		if newState.bossHP <= 0 {
			minMana = math.Min(minMana, newState.manaUsed)
			continue
		}

		// Calculate armor
		armor := 0
		for _, eff := range newState.effects {
			armor += eff.spell.armor
		}

		// Boss attacks
		newState.playerHP -= math.Max(1, bossAttack-armor)
		if newState.playerHP > 0 {
			simulate(newState, bossAttack)
		}
	}
}

func solvePart2(lines []string) int {
	bossHP := input.ParseInts(lines[0])[0]
	bossAttack := input.ParseInts(lines[1])[0]

	minMana = 1000000
	state := &State{
		playerHP:   50,
		playerMana: 500,
		bossHP:     bossHP,
		manaUsed:   0,
		effects:    []Effect{},
	}

	simulate(state, bossAttack)
	return minMana
}

func main() {
	inputPath := input.GetInputPath(2015, 22)
	lines := input.MustReadLines(inputPath)

	answer := solvePart2(lines)
	utils.PrintSolution(2, answer)
}
