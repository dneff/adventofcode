// Package grid provides a generic 2D grid type with common operations.
package grid

import (
	"fmt"
	"strings"

	"github.com/dneff/adventofcode/go/pkg/point"
)

// Grid represents a 2D grid of values of type T.
type Grid[T any] struct {
	cells  [][]T
	width  int
	height int
}

// New creates a new grid with the given dimensions.
// All cells are initialized to the zero value of type T.
func New[T any](width, height int) *Grid[T] {
	cells := make([][]T, height)
	for i := range cells {
		cells[i] = make([]T, width)
	}
	return &Grid[T]{
		cells:  cells,
		width:  width,
		height: height,
	}
}

// FromSlice creates a grid from a 2D slice.
func FromSlice[T any](cells [][]T) *Grid[T] {
	if len(cells) == 0 {
		return &Grid[T]{cells: [][]T{}, width: 0, height: 0}
	}
	height := len(cells)
	width := len(cells[0])
	return &Grid[T]{
		cells:  cells,
		width:  width,
		height: height,
	}
}

// FromRunes creates a grid from a slice of rune slices.
func FromRunes(cells [][]rune) *Grid[rune] {
	return FromSlice(cells)
}

// FromLines creates a rune grid from a slice of strings.
func FromLines(lines []string) *Grid[rune] {
	if len(lines) == 0 {
		return &Grid[rune]{cells: [][]rune{}, width: 0, height: 0}
	}
	height := len(lines)
	width := len(lines[0])
	cells := make([][]rune, height)
	for i, line := range lines {
		cells[i] = []rune(line)
	}
	return &Grid[rune]{
		cells:  cells,
		width:  width,
		height: height,
	}
}

// Width returns the width of the grid.
func (g *Grid[T]) Width() int {
	return g.width
}

// Height returns the height of the grid.
func (g *Grid[T]) Height() int {
	return g.height
}

// Get returns the value at the given point.
// Panics if the point is out of bounds.
func (g *Grid[T]) Get(p point.Point) T {
	return g.cells[p.Y][p.X]
}

// Set sets the value at the given point.
// Panics if the point is out of bounds.
func (g *Grid[T]) Set(p point.Point, value T) {
	g.cells[p.Y][p.X] = value
}

// GetXY returns the value at the given coordinates.
func (g *Grid[T]) GetXY(x, y int) T {
	return g.cells[y][x]
}

// SetXY sets the value at the given coordinates.
func (g *Grid[T]) SetXY(x, y int, value T) {
	g.cells[y][x] = value
}

// Contains checks if a point is within the grid bounds.
func (g *Grid[T]) Contains(p point.Point) bool {
	return p.X >= 0 && p.X < g.width && p.Y >= 0 && p.Y < g.height
}

// ContainsXY checks if coordinates are within the grid bounds.
func (g *Grid[T]) ContainsXY(x, y int) bool {
	return x >= 0 && x < g.width && y >= 0 && y < g.height
}

// Find returns the first point where the value equals the given value.
// Returns the point and true if found, otherwise returns zero point and false.
func (g *Grid[T]) Find(value T, equals func(T, T) bool) (point.Point, bool) {
	for y := 0; y < g.height; y++ {
		for x := 0; x < g.width; x++ {
			if equals(g.cells[y][x], value) {
				return point.New(x, y), true
			}
		}
	}
	return point.Point{}, false
}

// FindAll returns all points where the value matches the predicate.
func (g *Grid[T]) FindAll(predicate func(T) bool) []point.Point {
	var points []point.Point
	for y := 0; y < g.height; y++ {
		for x := 0; x < g.width; x++ {
			if predicate(g.cells[y][x]) {
				points = append(points, point.New(x, y))
			}
		}
	}
	return points
}

// Neighbors4 returns the 4 orthogonal neighbors of a point that are within bounds.
func (g *Grid[T]) Neighbors4(p point.Point) []point.Point {
	var neighbors []point.Point
	for _, dir := range point.Cardinal4 {
		next := p.Add(dir)
		if g.Contains(next) {
			neighbors = append(neighbors, next)
		}
	}
	return neighbors
}

// Neighbors8 returns the 8 neighbors (including diagonals) that are within bounds.
func (g *Grid[T]) Neighbors8(p point.Point) []point.Point {
	var neighbors []point.Point
	for _, dir := range point.Cardinal8 {
		next := p.Add(dir)
		if g.Contains(next) {
			neighbors = append(neighbors, next)
		}
	}
	return neighbors
}

// AllPoints returns all points in the grid.
func (g *Grid[T]) AllPoints() []point.Point {
	points := make([]point.Point, 0, g.width*g.height)
	for y := 0; y < g.height; y++ {
		for x := 0; x < g.width; x++ {
			points = append(points, point.New(x, y))
		}
	}
	return points
}

// Count returns the number of cells that match the predicate.
func (g *Grid[T]) Count(predicate func(T) bool) int {
	count := 0
	for y := 0; y < g.height; y++ {
		for x := 0; x < g.width; x++ {
			if predicate(g.cells[y][x]) {
				count++
			}
		}
	}
	return count
}

// Clone creates a deep copy of the grid.
func (g *Grid[T]) Clone() *Grid[T] {
	cells := make([][]T, g.height)
	for i := range cells {
		cells[i] = make([]T, g.width)
		copy(cells[i], g.cells[i])
	}
	return &Grid[T]{
		cells:  cells,
		width:  g.width,
		height: g.height,
	}
}

// String returns a string representation of the grid.
// For rune grids, this will display the characters.
func (g *Grid[T]) String() string {
	var sb strings.Builder
	for y := 0; y < g.height; y++ {
		for x := 0; x < g.width; x++ {
			sb.WriteString(fmt.Sprintf("%v", g.cells[y][x]))
		}
		if y < g.height-1 {
			sb.WriteRune('\n')
		}
	}
	return sb.String()
}

// ForEach applies a function to each cell in the grid.
func (g *Grid[T]) ForEach(fn func(point.Point, T)) {
	for y := 0; y < g.height; y++ {
		for x := 0; x < g.width; x++ {
			fn(point.New(x, y), g.cells[y][x])
		}
	}
}

// Map creates a new grid by applying a function to each cell.
func Map[T, U any](g *Grid[T], fn func(T) U) *Grid[U] {
	cells := make([][]U, g.height)
	for y := 0; y < g.height; y++ {
		cells[y] = make([]U, g.width)
		for x := 0; x < g.width; x++ {
			cells[y][x] = fn(g.cells[y][x])
		}
	}
	return &Grid[U]{
		cells:  cells,
		width:  g.width,
		height: g.height,
	}
}
