package main

// Advent of Code 2015 - Day 4: The Ideal Stocking Stuffer
// https://adventofcode.com/2015/day/4
//
// Find the lowest positive number that, when combined with the secret key,
// produces an MD5 hash starting with five zeros.

import (
	"crypto/md5"
	"fmt"
	"strconv"
	"strings"

	"github.com/dneff/adventofcode/go/pkg/input"
	"github.com/dneff/adventofcode/go/pkg/utils"
)

func solvePart1(secretKey string) int {
	suffix := 0
	for {
		possible := secretKey + strconv.Itoa(suffix)
		hash := md5.Sum([]byte(possible))
		hashStr := fmt.Sprintf("%x", hash)
		if strings.HasPrefix(hashStr, "00000") {
			return suffix
		}
		suffix++
	}
}

func main() {
	inputPath := input.GetInputPath(2015, 4)
	content := input.MustReadFile(inputPath)
	content = strings.TrimSpace(content)

	answer := solvePart1(content)
	utils.PrintSolution(1, answer)
}
