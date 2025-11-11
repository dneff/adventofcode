package main

// Advent of Code 2015 - Day 9: All in a Single Night
// https://adventofcode.com/2015/day/9
//
// Find the shortest route that visits every city exactly once.
// Classic traveling salesman problem.

import (
	"strings"

	"github.com/dneff/adventofcode/go/pkg/input"
	"github.com/dneff/adventofcode/go/pkg/math"
	"github.com/dneff/adventofcode/go/pkg/utils"
)

type Graph struct {
	cities    []string
	distances map[[2]string]int
}

func NewGraph() *Graph {
	return &Graph{
		cities:    make([]string, 0),
		distances: make(map[[2]string]int),
	}
}

func (g *Graph) addCity(city string) {
	if !utils.Contains(g.cities, city) {
		g.cities = append(g.cities, city)
	}
}

func (g *Graph) addDistance(from, to string, distance int) {
	g.addCity(from)
	g.addCity(to)
	g.distances[[2]string{from, to}] = distance
	g.distances[[2]string{to, from}] = distance
}

func (g *Graph) getDistance(from, to string) int {
	return g.distances[[2]string{from, to}]
}

func (g *Graph) routeDistance(route []string) int {
	total := 0
	for i := 0; i < len(route)-1; i++ {
		total += g.getDistance(route[i], route[i+1])
	}
	return total
}

func solvePart1(lines []string) int {
	graph := NewGraph()

	for _, line := range lines {
		line = strings.TrimSpace(line)
		parts := strings.Split(line, " = ")
		distance := input.ParseInt(parts[1])
		cities := strings.Split(parts[0], " to ")
		graph.addDistance(cities[0], cities[1], distance)
	}

	// Generate all permutations and find shortest
	routes := utils.Permute(graph.cities)
	shortest := -1

	for _, route := range routes {
		dist := graph.routeDistance(route)
		if shortest == -1 || dist < shortest {
			shortest = dist
		}
	}

	return shortest
}

func main() {
	inputPath := input.GetInputPath(2015, 9)
	lines := input.MustReadLines(inputPath)

	answer := solvePart1(lines)
	utils.PrintSolution(1, answer)
}
