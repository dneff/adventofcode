package advent

import "strconv"

func GetInt(s string) int {
	result, err := strconv.Atoi(s)
	Check(err)
	return result
}
