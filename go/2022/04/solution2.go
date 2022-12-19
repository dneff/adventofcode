package main

import (
	advent "advent/helpers"
	"bufio"
	"fmt"
	"os"
	"strings"
)

type Elf struct {
	min int
	max int
}

func Seperators(r rune) bool {
	return r == ',' || r == '-'
}

func elvesOverlap(elf1 *Elf, elf2 *Elf) bool {
	var overlap bool
	if elf2.min >= elf1.min && elf2.min <= elf1.max {
		overlap = true
	}
	if elf2.max >= elf1.min && elf2.max <= elf1.max {
		overlap = true
	}
	if elf1.min >= elf2.min && elf1.min <= elf2.max {
		overlap = true
	}
	if elf1.max >= elf2.min && elf1.max <= elf2.max {
		overlap = true
	}
	return overlap
}

func main() {
	file, err := os.Open("input/04.txt")
	advent.Check(err)
	defer file.Close()

	overlap := 0

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		values := strings.FieldsFunc(line, Seperators)

		elf1 := Elf{}
		elf1.min = advent.GetInt(values[0])
		elf1.max = advent.GetInt(values[1])

		elf2 := Elf{}
		elf2.min = advent.GetInt(values[2])
		elf2.max = advent.GetInt(values[3])

		if elvesOverlap(&elf1, &elf2) {
			overlap += 1
		}
	}

	fmt.Printf("The solution is: %v\n", overlap)
}
