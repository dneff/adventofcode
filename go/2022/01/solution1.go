package main

import (
	"bufio"
	"fmt"
	"os"
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
	maxEnergy := 0
	for _, val := range elves {
		if val > maxEnergy {
			maxEnergy = val
		}
	}
	fmt.Printf("The solution is: %v \n", maxEnergy)
}
