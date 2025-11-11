// Package pathfinding provides graph search algorithms like BFS and Dijkstra.
package pathfinding

import (
	"container/heap"
)

// State represents a generic state in a search problem.
// It must be comparable (can be used as a map key).
type State interface {
	comparable
}

// BFS performs breadth-first search to find the shortest path.
// Returns the distance to the goal, or -1 if no path exists.
//
// Parameters:
//   - start: the starting state
//   - goal: a function that returns true if the state is a goal
//   - neighbors: a function that returns all neighbors of a state
func BFS[S State](start S, goal func(S) bool, neighbors func(S) []S) int {
	if goal(start) {
		return 0
	}

	visited := make(map[S]bool)
	queue := []S{start}
	visited[start] = true
	distance := 0

	for len(queue) > 0 {
		distance++
		size := len(queue)

		for i := 0; i < size; i++ {
			current := queue[0]
			queue = queue[1:]

			for _, next := range neighbors(current) {
				if visited[next] {
					continue
				}
				if goal(next) {
					return distance
				}
				visited[next] = true
				queue = append(queue, next)
			}
		}
	}

	return -1
}

// BFSPath performs breadth-first search and returns the path to the goal.
// Returns the path as a slice of states, or nil if no path exists.
func BFSPath[S State](start S, goal func(S) bool, neighbors func(S) []S) []S {
	if goal(start) {
		return []S{start}
	}

	visited := make(map[S]bool)
	parent := make(map[S]S)
	queue := []S{start}
	visited[start] = true

	var endState S
	found := false

	for len(queue) > 0 && !found {
		current := queue[0]
		queue = queue[1:]

		for _, next := range neighbors(current) {
			if visited[next] {
				continue
			}
			visited[next] = true
			parent[next] = current

			if goal(next) {
				endState = next
				found = true
				break
			}
			queue = append(queue, next)
		}
	}

	if !found {
		return nil
	}

	// Reconstruct path
	var path []S
	for state := endState; ; state = parent[state] {
		path = append(path, state)
		if state == start {
			break
		}
	}

	// Reverse path
	for i, j := 0, len(path)-1; i < j; i, j = i+1, j-1 {
		path[i], path[j] = path[j], path[i]
	}

	return path
}

// BFSAll performs breadth-first search and visits all reachable states.
// Returns a map of states to their distances from the start.
func BFSAll[S State](start S, neighbors func(S) []S) map[S]int {
	distances := make(map[S]int)
	queue := []S{start}
	distances[start] = 0

	for len(queue) > 0 {
		current := queue[0]
		queue = queue[1:]
		currentDist := distances[current]

		for _, next := range neighbors(current) {
			if _, visited := distances[next]; visited {
				continue
			}
			distances[next] = currentDist + 1
			queue = append(queue, next)
		}
	}

	return distances
}

// Edge represents a weighted edge to a neighbor state.
type Edge[S State] struct {
	State S
	Cost  int
}

// priorityQueueItem is an item in the priority queue.
type priorityQueueItem[S State] struct {
	state    S
	priority int
	index    int
}

// priorityQueue implements heap.Interface.
type priorityQueue[S State] []*priorityQueueItem[S]

func (pq priorityQueue[S]) Len() int { return len(pq) }

func (pq priorityQueue[S]) Less(i, j int) bool {
	return pq[i].priority < pq[j].priority
}

func (pq priorityQueue[S]) Swap(i, j int) {
	pq[i], pq[j] = pq[j], pq[i]
	pq[i].index = i
	pq[j].index = j
}

func (pq *priorityQueue[S]) Push(x interface{}) {
	n := len(*pq)
	item := x.(*priorityQueueItem[S])
	item.index = n
	*pq = append(*pq, item)
}

func (pq *priorityQueue[S]) Pop() interface{} {
	old := *pq
	n := len(old)
	item := old[n-1]
	old[n-1] = nil
	item.index = -1
	*pq = old[0 : n-1]
	return item
}

// Dijkstra performs Dijkstra's algorithm to find the shortest weighted path.
// Returns the minimum cost to reach the goal, or -1 if no path exists.
//
// Parameters:
//   - start: the starting state
//   - goal: a function that returns true if the state is a goal
//   - neighbors: a function that returns weighted edges to neighbors
func Dijkstra[S State](start S, goal func(S) bool, neighbors func(S) []Edge[S]) int {
	if goal(start) {
		return 0
	}

	dist := make(map[S]int)
	pq := make(priorityQueue[S], 0)
	heap.Init(&pq)

	dist[start] = 0
	heap.Push(&pq, &priorityQueueItem[S]{state: start, priority: 0})

	for pq.Len() > 0 {
		item := heap.Pop(&pq).(*priorityQueueItem[S])
		current := item.state
		currentDist := item.priority

		// Skip if we've found a better path
		if d, ok := dist[current]; ok && currentDist > d {
			continue
		}

		if goal(current) {
			return currentDist
		}

		for _, edge := range neighbors(current) {
			newDist := currentDist + edge.Cost
			if oldDist, ok := dist[edge.State]; !ok || newDist < oldDist {
				dist[edge.State] = newDist
				heap.Push(&pq, &priorityQueueItem[S]{state: edge.State, priority: newDist})
			}
		}
	}

	return -1
}

// DijkstraAll performs Dijkstra's algorithm and returns distances to all reachable states.
// Returns a map of states to their minimum costs from the start.
func DijkstraAll[S State](start S, neighbors func(S) []Edge[S]) map[S]int {
	dist := make(map[S]int)
	pq := make(priorityQueue[S], 0)
	heap.Init(&pq)

	dist[start] = 0
	heap.Push(&pq, &priorityQueueItem[S]{state: start, priority: 0})

	for pq.Len() > 0 {
		item := heap.Pop(&pq).(*priorityQueueItem[S])
		current := item.state
		currentDist := item.priority

		// Skip if we've found a better path
		if d, ok := dist[current]; ok && currentDist > d {
			continue
		}

		for _, edge := range neighbors(current) {
			newDist := currentDist + edge.Cost
			if oldDist, ok := dist[edge.State]; !ok || newDist < oldDist {
				dist[edge.State] = newDist
				heap.Push(&pq, &priorityQueueItem[S]{state: edge.State, priority: newDist})
			}
		}
	}

	return dist
}

// DijkstraPath performs Dijkstra's algorithm and returns the path to the goal.
// Returns the path as a slice of states, or nil if no path exists.
func DijkstraPath[S State](start S, goal func(S) bool, neighbors func(S) []Edge[S]) []S {
	if goal(start) {
		return []S{start}
	}

	dist := make(map[S]int)
	parent := make(map[S]S)
	pq := make(priorityQueue[S], 0)
	heap.Init(&pq)

	dist[start] = 0
	heap.Push(&pq, &priorityQueueItem[S]{state: start, priority: 0})

	var endState S
	found := false

	for pq.Len() > 0 && !found {
		item := heap.Pop(&pq).(*priorityQueueItem[S])
		current := item.state
		currentDist := item.priority

		// Skip if we've found a better path
		if d, ok := dist[current]; ok && currentDist > d {
			continue
		}

		if goal(current) {
			endState = current
			found = true
			break
		}

		for _, edge := range neighbors(current) {
			newDist := currentDist + edge.Cost
			if oldDist, ok := dist[edge.State]; !ok || newDist < oldDist {
				dist[edge.State] = newDist
				parent[edge.State] = current
				heap.Push(&pq, &priorityQueueItem[S]{state: edge.State, priority: newDist})
			}
		}
	}

	if !found {
		return nil
	}

	// Reconstruct path
	var path []S
	for state := endState; ; state = parent[state] {
		path = append(path, state)
		if state == start {
			break
		}
	}

	// Reverse path
	for i, j := 0, len(path)-1; i < j; i, j = i+1, j-1 {
		path[i], path[j] = path[j], path[i]
	}

	return path
}
