// Package point provides 2D point types and operations for grid-based puzzles.
package point

import "fmt"

// Point represents a 2D coordinate (x, y) or (col, row).
type Point struct {
	X, Y int
}

// New creates a new Point with the given coordinates.
func New(x, y int) Point {
	return Point{X: x, Y: y}
}

// Add returns the sum of two points (vector addition).
func (p Point) Add(other Point) Point {
	return Point{X: p.X + other.X, Y: p.Y + other.Y}
}

// Sub returns the difference of two points (vector subtraction).
func (p Point) Sub(other Point) Point {
	return Point{X: p.X - other.X, Y: p.Y - other.Y}
}

// Mul returns the point scaled by a scalar value.
func (p Point) Mul(scalar int) Point {
	return Point{X: p.X * scalar, Y: p.Y * scalar}
}

// Manhattan returns the Manhattan distance between two points.
func (p Point) Manhattan(other Point) int {
	dx := p.X - other.X
	dy := p.Y - other.Y
	if dx < 0 {
		dx = -dx
	}
	if dy < 0 {
		dy = -dy
	}
	return dx + dy
}

// ManhattanFromOrigin returns the Manhattan distance from the origin.
func (p Point) ManhattanFromOrigin() int {
	return p.Manhattan(Point{0, 0})
}

// String returns a string representation of the point.
func (p Point) String() string {
	return fmt.Sprintf("(%d,%d)", p.X, p.Y)
}

// Neighbors4 returns the 4 orthogonal neighbors (up, down, left, right).
func (p Point) Neighbors4() []Point {
	return []Point{
		p.Add(North),
		p.Add(South),
		p.Add(East),
		p.Add(West),
	}
}

// Neighbors8 returns all 8 neighbors (including diagonals).
func (p Point) Neighbors8() []Point {
	return []Point{
		p.Add(North),
		p.Add(NorthEast),
		p.Add(East),
		p.Add(SouthEast),
		p.Add(South),
		p.Add(SouthWest),
		p.Add(West),
		p.Add(NorthWest),
	}
}

// RotateLeft rotates the point 90 degrees counterclockwise around the origin.
func (p Point) RotateLeft() Point {
	return Point{X: p.Y, Y: -p.X}
}

// RotateRight rotates the point 90 degrees clockwise around the origin.
func (p Point) RotateRight() Point {
	return Point{X: -p.Y, Y: p.X}
}

// Direction vectors for the four cardinal directions.
// In grid coordinates: North is up (negative Y), South is down (positive Y).
var (
	North = Point{X: 0, Y: -1}
	South = Point{X: 0, Y: 1}
	East  = Point{X: 1, Y: 0}
	West  = Point{X: -1, Y: 0}
)

// Direction vectors for the eight cardinal and diagonal directions.
var (
	NorthEast = Point{X: 1, Y: -1}
	SouthEast = Point{X: 1, Y: 1}
	SouthWest = Point{X: -1, Y: 1}
	NorthWest = Point{X: -1, Y: -1}
)

// Cardinal4 returns all 4 cardinal directions.
var Cardinal4 = []Point{North, East, South, West}

// Cardinal8 returns all 8 directions (cardinal + diagonal).
var Cardinal8 = []Point{North, NorthEast, East, SouthEast, South, SouthWest, West, NorthWest}

// TurnLeft returns the direction after turning left (counterclockwise).
func TurnLeft(dir Point) Point {
	switch dir {
	case North:
		return West
	case West:
		return South
	case South:
		return East
	case East:
		return North
	default:
		return dir.RotateLeft()
	}
}

// TurnRight returns the direction after turning right (clockwise).
func TurnRight(dir Point) Point {
	switch dir {
	case North:
		return East
	case East:
		return South
	case South:
		return West
	case West:
		return North
	default:
		return dir.RotateRight()
	}
}

// Reverse returns the opposite direction.
func Reverse(dir Point) Point {
	return Point{X: -dir.X, Y: -dir.Y}
}

// ParseDirection converts a character to a direction vector.
// Accepts: 'N', 'S', 'E', 'W', 'U', 'D', 'L', 'R', '^', 'v', '<', '>'
func ParseDirection(ch rune) Point {
	switch ch {
	case 'N', 'U', '^':
		return North
	case 'S', 'D', 'v':
		return South
	case 'E', 'R', '>':
		return East
	case 'W', 'L', '<':
		return West
	default:
		panic(fmt.Sprintf("unknown direction: %c", ch))
	}
}
