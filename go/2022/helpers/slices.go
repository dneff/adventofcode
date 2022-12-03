package advent

func Sum(ints *[]int) int {
	sum := 0
	for _, x := range *ints {
		sum += x
	}
	return sum
}

func Max(ints *[]int) int {
	max := (*ints)[0]
	for _, x := range *ints {
		if x > max {
			max = x
		}
	}
	return max
}
