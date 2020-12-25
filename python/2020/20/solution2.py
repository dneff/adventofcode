import math
from collections import defaultdict
import numpy as np


def printSolution(x):
    print(f"The solution is: {x}")


class Tile:
    def __init__(self):
        self.id = None
        self.data = []
        self.edges = {}
        self.connecting = []

    def getEdges(self):
        top, bottom = self.data[0], self.data[-1]
        left, right = [x[0] for x in self.data], [x[-1] for x in self.data]
        orientation = {"top": top, "bottom": bottom, "left": left, "right": right}
        for k, v in orientation.items():
            self.edges[k] = self.findValue(v)
            self.edges[k + "_reverse"] = self.findValue(v[::-1])
        return self.edges

    def rotate(self):
        tmp = np.array(self.data)
        tmp = np.rot90(tmp)
        self.data = tmp.tolist()
        self.getEdges()

    def flipSide(self):
        tmp = np.array(self.data)
        tmp = np.fliplr(tmp)
        self.data = tmp.tolist()
        self.getEdges()

    def flipUp(self):
        tmp = np.array(self.data)
        tmp = np.flipud(tmp)
        self.data = tmp.tolist()
        self.getEdges()

    def findValue(self, row):
        return int("".join(row), 2)

    def __repr__(self):
        return repr(f"Tile: {self.id}, {self.data}")


def main():
    file = open("input.txt", "r")

    t = Tile()
    tiles = []
    for line in file:
        line = line.strip()
        if not line:
            t.getEdges()
            tiles.append(t)
            t = Tile()
        elif "Tile" in line:
            t.id = int("".join(filter(str.isdigit, line)))
        else:
            t.data.append(["1" if x == "#" else "0" for x in line])

    t.getEdges()
    tiles.append(t)

    for t in tiles:
        for t_check in tiles:
            if t.id == t_check.id:
                continue
            else:
                c = set(t.edges.values()).intersection(set(t_check.edges.values()))
                if len(c):
                    t.connecting.append(t_check.id)

    corners = [t for t in tiles if len(t.connecting) == 2]

    # create an appropriately sized grid
    pic_side = int(math.sqrt(len(tiles)))
    grid = [[0] * pic_side for x in range(pic_side)]

    r = False
    b = False
    top_corner = None
    while not top_corner:
        for c in corners:
            for t in tiles:
                if t.id in c.connecting:
                    for k, v in c.edges.items():
                        if v in t.edges.values():
                            if k == "left":
                                r = True
                            elif k == "bottom":
                                b = True
            if r and b:
                top_corner = c
                break
            else:
                r = False
                b = False

        for c in corners:
            c.rotate()
            c.getEdges()

    t = top_corner
    current_loc = [0, 0]
    grid[current_loc[0]][current_loc[1]] = t
    tiles.remove(t)
    grid[current_loc[0]][current_loc[1]].getEdges()

    current_loc[0] += 1
    print("--ordering, rotating, flipping tiles")
    while True:
        row, col = current_loc
        if row == pic_side:
            row, col = current_loc = [0, col + 1]
            if col == pic_side:
                break
        if row == 0:
            # find left match
            finder = grid[row][col - 1].edges["right"]
            for t in tiles:
                if finder in t.edges.values():
                    while finder not in [t.edges["left"], t.edges["left_reverse"]]:
                        t.rotate()
                    while finder != t.edges["left"]:
                        t.flipUp()
                    grid[row][col] = t
                    tiles.remove(t)
                    break

        else:
            # find top match
            finder = grid[row - 1][col].edges["bottom"]
            for t in tiles:
                if finder in t.edges.values():
                    while finder not in [t.edges["top"], t.edges["top_reverse"]]:
                        t.rotate()
                    while finder != t.edges["top"]:
                        t.flipSide()
                    grid[row][col] = t
                    tiles.remove(t)
                    break

        current_loc = [row + 1, col]

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            t = grid[row][col]

    print("--trimming tiles to array")
    # yay, move grid to numpy array
    image = defaultdict(list)
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            for line in range(1, len(grid[row][col].data) - 1):
                image[(row, line)].extend(grid[row][col].data[line][1:-1])

    photo = np.array([image[x] for x in sorted(image.keys())], dtype=int)

    monster_data = [
        "                  # ",
        "#    ##    ##    ###",
        " #  #  #  #  #  #   ",
    ]

    monster = []
    for line in monster_data:
        monster.append([1 if x == "#" else -1 for x in line])
    monster = np.array(monster, dtype=int)
    monster_mask = monster > 0
    m_length = len(monster)
    m_height = len(monster[0])

    print("--sea monster hunting")
    monster_count = 0
    rotations = 0

    while monster_count < 1:
        for row in range(len(photo) - m_length + 1):
            for col in range(len(photo[0]) - m_height + 1):
                snapshot = np.array(photo[row : row + m_length, col : col + m_height])

                if np.sum(snapshot == monster) == 15:
                    monster_count += 1

                    snapshot[snapshot == monster] = 0
                    photo[row : row + m_length, col : col + m_height][monster_mask] = snapshot[monster_mask]

        if monster_count == 0:
            if rotations < 5:
                photo = np.rot90(photo)
                rotations += 1
            else:
                photo = np.flipud(photo)
                rotations = 0
        else:
            break

    for row in range(len(photo) - m_length + 1):
        for col in range(len(photo[0]) - m_height + 1):
            snapshot = np.array(photo[row : row + m_length, col : col + m_height])

    photo_pixels = sum(sum(photo))
    printSolution(photo_pixels)


if __name__ == "__main__":
    main()
