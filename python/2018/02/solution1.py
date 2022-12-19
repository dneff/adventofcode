
def printSolution(x):
    print(f"The solution is {x}")

def main():

    two = set()
    three = set()

    file = open('input.txt', 'r')
    for line in file.readlines():
        box_id = line.strip()
        for c in box_id:
            if box_id not in two or box_id not in three:
                char_count = box_id.count(c)
                if char_count == 2:
                    two.add(box_id)
                elif char_count == 3:
                    three.add(box_id)

    
    printSolution(len(two) * len(three))

if __name__ == "__main__":
    main()