package advent

func Sum(ints *[]int) int {
	sum := 0
	for _, x := range *ints {
		sum += x
	}
	return sum
}

func Min(ints *[]int) int {
	min := (*ints)[0]
	for _, x := range *ints {
		if x < min {
			min = x
		}
	}
	return min
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
