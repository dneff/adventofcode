
def printSolution(x):
    print(f"The solution is {x}")

def main():

    boxes  = []

    file = open('input.txt', 'r')
    for line in file.readlines():
        box_id = line.strip()
        for seen_id in boxes:
            mismatch = sum([1 for x,y in zip(box_id, seen_id) if x != y])
            if mismatch == 1:
                solution = [x for x,y in zip(box_id, seen_id) if x==y]
                printSolution(''.join(solution))
                break
        boxes.append(box_id)


if __name__ == "__main__":
    main()