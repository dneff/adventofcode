
def printSolution(x):
    print(f"The solution is: {x}")

direction = {
    "U":(0,1),
    "R":(1,0),
    "D":(0,-1),
    "L":(-1,0),
}

#function to update the position of the head
def updatePosition(position, heading):
    delta = direction[heading]
    return (position[0] + delta[0], position[1] + delta[1])

#function to check if two points are adjacent
def isAdjacent(head, tail):
    offset = (abs(head[0] - tail[0]), abs(head[1] - tail[1]))
    return max(offset) < 2

#function to update the tail position by moving it one step closer to the head
def updateTail(head, tail):
    if head[0] > tail[0]:
        tail = (tail[0] + 1, tail[1])
    elif head[0] < tail[0]:
        tail = (tail[0] - 1, tail[1])
    if head[1] > tail[1]:
        tail = (tail[0], tail[1] + 1)
    elif head[1] < tail[1]:
        tail = (tail[0], tail[1] - 1)
    return tail

def main():
    file = open('../input/09.txt', 'r', encoding='utf-8')
    H_pos = (0,0)
    T_pos = (0,0)
    H_moves = [H_pos]
    T_moves = [T_pos]
    for line in file.readlines():
        heading, count = line.strip().split()
        count = int(count)
        for _ in range(count):
            H_pos = updatePosition(H_pos, heading)
            if not isAdjacent(H_pos, T_pos):
                T_pos = updateTail(H_pos, T_pos)
            print(f"H: {H_pos}, T:{T_pos}")
            
            H_moves.append(H_pos)
            T_moves.append(T_pos)

    printSolution(len(set(T_moves)))

if __name__ == "__main__":
    main()