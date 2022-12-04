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

func matchCharacterThree(first *string, second *string, third *string) string {
	for _, c1 := range *first {
		for _, c2 := range *second {
			for _, c3 := range *third {
				if c1 == c2 && c2 == c3 {
					return string(c1)
				}
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
	var rucksack []string
	var badges []int
	for scanner.Scan() {
		line := scanner.Text()
		rucksack = append(rucksack, line)
		if len(rucksack)%3 == 0 {
			first := &rucksack[len(rucksack)-3]
			second := &rucksack[len(rucksack)-2]
			third := &rucksack[len(rucksack)-1]

			char := matchCharacterThree(first, second, third)
			fmt.Printf("The match is: %v \n", char)
			score := characterValue(&char)
			fmt.Printf("The score is: %v\n", score)
			badges = append(badges, score)
		}

	}
	solution := advent.Sum(&badges)
	fmt.Printf("The solution is: %v", solution)
}
