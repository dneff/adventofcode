package main

import (
	advent "advent/helpers"
	"bufio"
	"fmt"
	"os"
	"sort"
	"strconv"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func main() {
	var elves []int
	elves = append(elves, 0)

	file, err := os.Open("input/01.txt")
	check(err)
	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		energy := scanner.Text()
		if energy == "" {
			elves = append(elves, 0)
		} else {
			energyVal, err := strconv.Atoi(energy)
			check(err)
			elves[len(elves)-1] += energyVal
		}
	}
	sort.Ints(elves)
	top3 := elves[len(elves)-3:]

	fmt.Printf("The solution is: %v \n", advent.Sum(&top3))

}
