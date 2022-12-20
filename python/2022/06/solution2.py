
def printSolution(x):
    print(f"The solution is: {x}")

def markerEnd(s, size=4):
    marker = []
    for idx, char in enumerate(s):
        marker.append(char)
        if len(marker) < size:
            continue
        if len(marker) > size:
            marker = marker[-size:]
        if len(set(marker)) == size:
            return idx + 1
    return ValueError("No index found")


def main():
    file = open('../input/06.txt', 'r', encoding='utf-8')
    for line in file.readlines():
        end = markerEnd(line.strip(), 14)
        printSolution(end)

if __name__ == "__main__":
    main()