
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
    rope = [(0,0)] * 10
    T_moves = []
    T_moves.append(rope[-1])

    for line in file.readlines():
        heading, count = line.strip().split()
        count = int(count)
        for _ in range(count):
            for idx, pos in enumerate(rope):
                if idx == 0:
                    rope[idx] = updatePosition(pos, heading)
                else:
                    if not isAdjacent(pos, rope[idx-1]):
                        rope[idx] = updateTail(rope[idx-1], pos)

            print(f"H: {rope[0]}, T:{rope[-1]}")            
            T_moves.append(rope[-1])

    printSolution(len(set(T_moves)))

if __name__ == "__main__":
    main()