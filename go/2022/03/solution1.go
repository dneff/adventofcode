package main

import (
	advent "advent/helpers"
	"bufio"
	"fmt"
	"os"
)

func characterValue(char *string) int {
	charRune := []rune(*char)
	result := int(charRune[0])
	result -= 96
	if result <= 0 {
		result += 58
	}
	return result
}

func matchCharacter(first *string, last *string) string {
	for _, c1 := range *first {
		for _, c2 := range *last {
			if c1 == c2 {
				return string(c1)
			}
		}
	}
	panic("no matches!")
}

func main() {
	file, err := os.Open("input/03.txt")
	advent.Check(err)
	defer file.Close()

	scanner := bufio.NewScanner(file)
	var rucksack []int
	for scanner.Scan() {
		line := scanner.Text()
		first := line[:len(line)/2]
		last := line[len(line)/2:]
		fmt.Printf("first: %v , last: %v \n", first, last)
		char := matchCharacter(&first, &last)
		fmt.Printf("The match is: %v \n", char)
		score := characterValue(&char)
		fmt.Printf("The score is: %v\n", score)
		rucksack = append(rucksack, score)
	}
	solution := advent.Sum(&rucksack)
	fmt.Printf("The solution is: %v", solution)
}
