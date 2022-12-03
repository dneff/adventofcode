package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func handScore(hand string) int {
	switch hand {
	case "A":
		return 1
	case "B":
		return 2
	case "C":
		return 3
	case "X":
		return 1
	case "Y":
		return 2
	case "Z":
		return 3
	default:
		return 0
	}
}

func gameScore(us int, them int) int {
	win := 6
	draw := 3
	lose := 0

	if us == them {
		return us + draw
	}
	if (us == 1 && them == 3) || (us == 2 && them == 1) || (us == 3 && them == 2) {
		return us + win
	}
	return us + lose
}

func main() {
	file, err := os.Open("input/02.txt")
	check(err)
	defer file.Close()

	totalScore := 0
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		game := scanner.Text()
		game = strings.TrimSpace(game)
		hands := strings.Split(game, " ")
		them := handScore(hands[0])
		us := handScore(hands[1])
		fmt.Printf("us: %v - them: %v \n", us, them)
		result := gameScore(us, them)
		fmt.Printf("score: %v \n", result)
		totalScore += result
	}
	fmt.Printf("The solution is: %v \n", totalScore)
}
