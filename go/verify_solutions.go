package main

import (
	"bytes"
	"flag"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strconv"
	"strings"
	"time"
)

// ANSI color codes
const (
	colorReset  = "\033[0m"
	colorGreen  = "\033[92m"
	colorRed    = "\033[91m"
	colorYellow = "\033[93m"
	colorBlue   = "\033[94m"
)

// getTimeEmoji returns an emoji based on execution time
func getTimeEmoji(elapsedTime float64) string {
	switch {
	case elapsedTime < 1.0:
		return "⚡"
	case elapsedTime < 3.0:
		return "🚀"
	case elapsedTime < 10.0:
		return "▶️"
	case elapsedTime < 30.0:
		return "🐢"
	default:
		return "🐌"
	}
}

// getExpectedAnswer reads the expected answer from aoc-data directory
func getExpectedAnswer(year, day, part int) (string, bool) {
	answerFile := filepath.Join("..", "aoc-data", strconv.Itoa(year), strconv.Itoa(day), fmt.Sprintf("solution-%d", part))

	data, err := os.ReadFile(answerFile)
	if err != nil {
		return "", false
	}

	content := strings.TrimSpace(string(data))
	// Return false if empty or just '0'
	if content == "" || content == "0" {
		return "", false
	}

	return content, true
}

// writeAnswer writes an answer to the aoc-data directory
func writeAnswer(year, day, part int, answer string) bool {
	answerDir := filepath.Join("..", "aoc-data", strconv.Itoa(year), strconv.Itoa(day))
	answerFile := filepath.Join(answerDir, fmt.Sprintf("solution-%d", part))

	// Create directory if it doesn't exist
	if err := os.MkdirAll(answerDir, 0755); err != nil {
		fmt.Printf("%sError creating directory: %v%s\n", colorRed, err, colorReset)
		return false
	}

	// Write the answer
	if err := os.WriteFile(answerFile, []byte(strings.TrimSpace(answer)+"\n"), 0644); err != nil {
		fmt.Printf("%sError writing answer: %v%s\n", colorRed, err, colorReset)
		return false
	}

	return true
}

// runSolution runs a Go solution and extracts the answer
func runSolution(year, day, part int) (string, bool, float64, bool) {
	dayStr := fmt.Sprintf("%02d", day)
	solutionFile := filepath.Join(strconv.Itoa(year), dayStr, fmt.Sprintf("solution%d.go", part))

	// Check if file exists
	if _, err := os.Stat(solutionFile); os.IsNotExist(err) {
		return "", false, 0.0, false
	}

	// Run the solution
	startTime := time.Now()
	cmd := exec.Command("go", "run", solutionFile)
	cmd.Dir = "."

	var stdout, stderr bytes.Buffer
	cmd.Stdout = &stdout
	cmd.Stderr = &stderr

	err := cmd.Run()
	elapsedTime := time.Since(startTime).Seconds()

	if err != nil {
		return "", false, elapsedTime, true
	}

	// Extract the answer from output (looking for lines like "Part 1: 138")
	for _, line := range strings.Split(stdout.String(), "\n") {
		prefix := fmt.Sprintf("Part %d:", part)
		if strings.Contains(line, prefix) {
			answer := strings.TrimSpace(strings.Split(line, ":")[1])
			return answer, true, elapsedTime, true
		}
	}

	return "", false, elapsedTime, true
}

// getYearsToVerify returns the list of years to verify
func getYearsToVerify(year *int) []int {
	if year != nil {
		return []int{*year}
	}

	// Find all year directories
	entries, err := os.ReadDir(".")
	if err != nil {
		return []int{}
	}

	var years []int
	for _, entry := range entries {
		if !entry.IsDir() {
			continue
		}
		yearNum, err := strconv.Atoi(entry.Name())
		if err == nil && yearNum >= 2015 && yearNum <= 2024 {
			years = append(years, yearNum)
		}
	}

	// Sort years
	for i := 0; i < len(years); i++ {
		for j := i + 1; j < len(years); j++ {
			if years[i] > years[j] {
				years[i], years[j] = years[j], years[i]
			}
		}
	}

	return years
}

func main() {
	// Parse command-line arguments
	var yearPos int
	var dayPos int
	var yearFlag int
	var dayFlag int
	var writeMissing bool

	flag.IntVar(&yearFlag, "year", 0, "Year to verify (e.g., 2015)")
	flag.IntVar(&yearFlag, "y", 0, "Year to verify (short form)")
	flag.IntVar(&dayFlag, "day", 0, "Day to verify (1-25)")
	flag.IntVar(&dayFlag, "d", 0, "Day to verify (short form)")
	flag.BoolVar(&writeMissing, "write-missing", false, "Write solution output to missing answer files")
	flag.BoolVar(&writeMissing, "w", false, "Write solution output to missing answer files (short form)")

	flag.Parse()

	// Handle positional arguments
	args := flag.Args()
	if len(args) > 0 {
		if y, err := strconv.Atoi(args[0]); err == nil {
			yearPos = y
		}
	}
	if len(args) > 1 {
		if d, err := strconv.Atoi(args[1]); err == nil {
			dayPos = d
		}
	}

	// Prioritize positional arguments over flags
	var year *int
	if yearPos != 0 {
		year = &yearPos
	} else if yearFlag != 0 {
		year = &yearFlag
	}

	var day *int
	if dayPos != 0 {
		day = &dayPos
	} else if dayFlag != 0 {
		day = &dayFlag
	}

	// Validate day if specified
	if day != nil && (*day < 1 || *day > 25) {
		fmt.Printf("%sError: Day must be between 1 and 25%s\n", colorRed, colorReset)
		os.Exit(1)
	}

	yearsToVerify := getYearsToVerify(year)
	if len(yearsToVerify) == 0 {
		fmt.Printf("%sError: No Go solutions directories found%s\n", colorRed, colorReset)
		os.Exit(1)
	}

	// Determine days to verify
	var daysToVerify []int
	if day != nil {
		daysToVerify = []int{*day}
	} else {
		for i := 1; i <= 25; i++ {
			daysToVerify = append(daysToVerify, i)
		}
	}

	// Verify all years
	allTotalVerified := 0
	allTotalCorrect := 0
	allTotalIncorrect := 0
	allTotalMissing := 0
	allTotalFailed := 0

	for _, yearNum := range yearsToVerify {
		yearDir := strconv.Itoa(yearNum)
		aocDataDir := filepath.Join("..", "aoc-data", yearDir)

		if _, err := os.Stat(yearDir); os.IsNotExist(err) {
			fmt.Printf("%sError: Go solutions directory not found for year %d%s\n", colorRed, yearNum, colorReset)
			fmt.Printf("Expected directory: %s\n", yearDir)
			continue
		}

		if _, err := os.Stat(aocDataDir); os.IsNotExist(err) && !writeMissing {
			fmt.Printf("%sWarning: aoc-data directory not found for year %d%s\n", colorYellow, yearNum, colorReset)
			fmt.Printf("Expected directory: %s\n", aocDataDir)
			fmt.Println("Continuing anyway, but no answers will be verified.")
		}

		if len(yearsToVerify) > 1 {
			fmt.Printf("\n%sVerifying %d Advent of Code Solutions%s\n", colorBlue, yearNum, colorReset)
			fmt.Println(strings.Repeat("=", 60))
		} else {
			fmt.Printf("%sVerifying %d Advent of Code Solutions%s\n", colorBlue, yearNum, colorReset)
			fmt.Println(strings.Repeat("=", 60))
		}

		totalVerified := 0
		totalCorrect := 0
		totalIncorrect := 0
		totalMissing := 0
		totalFailed := 0
		totalWritten := 0

		for _, dayNum := range daysToVerify {
			for part := 1; part <= 2; part++ {
				expected, hasExpected := getExpectedAnswer(yearNum, dayNum, part)

				// Run the solution
				actual, success, elapsedTime, fileExists := runSolution(yearNum, dayNum, part)

				// Case 1: Solution file doesn't exist and answer file doesn't exist
				// -> Skip entirely, no output, no counting
				if !fileExists && !hasExpected {
					continue
				}

				// Case 2: Solution file doesn't exist but answer file exists
				// -> Show MISSING status (solution file is missing)
				if !fileExists && hasExpected {
					fmt.Printf("%s○%s Day %2d Part %d: %sMISSING%s (solution file not found)\n",
						colorYellow, colorReset, dayNum, part, colorYellow, colorReset)
					totalMissing++
					continue
				}

				// Case 3: Solution file exists but failed to run
				if fileExists && (!success || actual == "") {
					emoji := getTimeEmoji(elapsedTime)
					fmt.Printf("%s✗%s Day %2d Part %d: %sFAILED TO RUN%s (%.3fs) %s\n",
						colorRed, colorReset, dayNum, part, colorRed, colorReset, elapsedTime, emoji)
					totalFailed++
					continue
				}

				// Case 4: Solution ran successfully but no expected answer
				// -> Show MISSING status (answer is missing)
				if !hasExpected {
					emoji := getTimeEmoji(elapsedTime)
					statusMsg := fmt.Sprintf("%sMISSING%s", colorYellow, colorReset)

					// Write to answer file if requested
					if writeMissing {
						if writeAnswer(yearNum, dayNum, part, actual) {
							statusMsg = fmt.Sprintf("%sMISSING (wrote: %s)%s", colorYellow, actual, colorReset)
							totalWritten++
						} else {
							statusMsg = fmt.Sprintf("%sMISSING (failed to write)%s", colorYellow, colorReset)
						}
					}

					fmt.Printf("%s○%s Day %2d Part %d: %s (answer: %s, %.3fs) %s\n",
						colorYellow, colorReset, dayNum, part, statusMsg, actual, elapsedTime, emoji)
					totalMissing++
					continue
				}

				// Case 5: Solution ran successfully and has expected answer
				// -> Compare and show CORRECT/INCORRECT
				totalVerified++

				if actual == expected {
					emoji := getTimeEmoji(elapsedTime)
					fmt.Printf("%s✓%s Day %2d Part %d: %sCORRECT%s (answer: %s, %.3fs) %s\n",
						colorGreen, colorReset, dayNum, part, colorGreen, colorReset, actual, elapsedTime, emoji)
					totalCorrect++
				} else {
					emoji := getTimeEmoji(elapsedTime)
					fmt.Printf("%s✗%s Day %2d Part %d: %sINCORRECT%s (expected: %s, got: %s, %.3fs) %s\n",
						colorRed, colorReset, dayNum, part, colorRed, colorReset, expected, actual, elapsedTime, emoji)
					totalIncorrect++
				}
			}
		}

		// Print summary for this year
		fmt.Println()
		fmt.Println(strings.Repeat("=", 60))
		fmt.Printf("%sSummary for %d:%s\n", colorBlue, yearNum, colorReset)
		fmt.Printf("  %sCorrect:%s      %d\n", colorGreen, colorReset, totalCorrect)
		fmt.Printf("  %sIncorrect:%s    %d\n", colorRed, colorReset, totalIncorrect)
		fmt.Printf("  %sFailed:%s       %d\n", colorRed, colorReset, totalFailed)
		fmt.Printf("  %sMissing:%s      %d\n", colorYellow, colorReset, totalMissing)
		if writeMissing && totalWritten > 0 {
			fmt.Printf("  %sWritten:%s      %d\n", colorYellow, colorReset, totalWritten)
		}
		fmt.Printf("  %sTotal Verified:%s %d\n", colorBlue, colorReset, totalVerified)

		allTotalVerified += totalVerified
		allTotalCorrect += totalCorrect
		allTotalIncorrect += totalIncorrect
		allTotalMissing += totalMissing
		allTotalFailed += totalFailed
	}

	// Print overall summary if multiple years
	if len(yearsToVerify) > 1 {
		fmt.Println()
		fmt.Println(strings.Repeat("=", 60))
		fmt.Printf("%sOverall Summary:%s\n", colorBlue, colorReset)
		fmt.Printf("  %sCorrect:%s      %d\n", colorGreen, colorReset, allTotalCorrect)
		fmt.Printf("  %sIncorrect:%s    %d\n", colorRed, colorReset, allTotalIncorrect)
		fmt.Printf("  %sFailed:%s       %d\n", colorRed, colorReset, allTotalFailed)
		fmt.Printf("  %sMissing:%s      %d\n", colorYellow, colorReset, allTotalMissing)
		fmt.Printf("  %sTotal Verified:%s %d\n", colorBlue, colorReset, allTotalVerified)
	}

	if allTotalIncorrect > 0 || allTotalFailed > 0 {
		os.Exit(1)
	} else {
		if allTotalVerified > 0 {
			fmt.Printf("\n%sAll verified solutions are correct!%s\n", colorGreen, colorReset)
		} else {
			fmt.Printf("\n%sNo solutions were verified.%s\n", colorYellow, colorReset)
		}
	}
}
