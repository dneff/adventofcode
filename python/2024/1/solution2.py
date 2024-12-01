import collections

def print_solution(x):
    print(f"The solution is: {x}")



def main():
    """
    figure out exactly how often each number from the left list 
    appears in the right list. Calculate a total similarity score 
    by adding up each number in the left list after multiplying it 
    by the number of times that number appears in the right list.
    """
    left, right = [],[]
    filename = "./python/2024/input/01.txt"
    with open(filename, "r", encoding="utf-8") as f:
        for line in f.readlines():
            l, r = [int(x) for x in line.split()]
            left.append(l), right.append(r)

    freq = collections.Counter(right)
    score = [x * freq[x] for x in left]
    
    print_solution(sum(score))
    



if __name__ == "__main__":
    main()