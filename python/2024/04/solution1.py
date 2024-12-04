
def print_solution(x):
    """prints solution"""
    print(f"The solution is: {x}")

def get_word_count(word, line):
    """returns the number of times a word appears in a line"""
    if len(word) > len(line):
        return 0
    score = line.count(word)
    return score

def main():
    """finds solution"""
    filename = "./python/2024/input/04.txt"
    word = 'XMAS'
    input_data = []
    with open(filename, "r", encoding="utf-8") as f:
        word_count = 0
        puzzle = []
        for line in f.readlines():
            puzzle.append(list(line.strip()))
        # checks horizontal lines for word
        for line in puzzle:
            l = "".join(line)
            score = get_word_count(word, l)
            word_count += score
            l = l[::-1]
            score = get_word_count(word, l)
            word_count += score
        # checks vertical lines for word
        for i in range(len(puzzle[0])):
            l = "".join([puzzle[j][i] for j in range(len(puzzle))])
            score = get_word_count(word, l)
            word_count += score
            l = l[::-1]
            score = get_word_count(word, l)
            word_count += score
        # checks northwest to southeast diagonal lines for word
        for i in range(len(puzzle)):
            l = "".join([puzzle[i+j][j] for j in range(len(puzzle)-i)])
            score = get_word_count(word, l)
            word_count += score
            l = l[::-1]
            score = get_word_count(word, l)
            word_count += score
        for i in range(len(puzzle)):
            if i == 0:
                continue
            l = "".join([puzzle[j][j+i] for j in range(len(puzzle)-i)])
            score = get_word_count(word, l)
            word_count += score
            l = l[::-1]
            score = get_word_count(word, l)
            word_count += score
        # flip the puzzle and do it again
        puzzle = [x[::-1] for x in puzzle]
        for i in range(len(puzzle)):
            l = "".join([puzzle[i+j][j] for j in range(len(puzzle)-i)])
            score = get_word_count(word, l)
            word_count += score
            l = l[::-1]
            score = get_word_count(word, l)
            word_count += score
        for i in range(len(puzzle)):
            if i == 0:
                continue
            l = "".join([puzzle[j][j+i] for j in range(len(puzzle)-i)])
            score = get_word_count(word, l)
            word_count += score
            l = l[::-1]
            score = get_word_count(word, l)
            word_count += score

        print_solution(word_count)

if __name__ == "__main__":
    main()
