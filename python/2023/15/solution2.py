"""solves for day 15, 2023 part 2"""
from collections import defaultdict


def print_solution(x):
    """prints solution"""
    print(f"The solution is: {x}")


def hash(s):
    """hashed value of x"""
    value = 0
    for c in s:
        value += ord(c)
        value *= 17
        value = value % 256
    return value


def main():
    """load puzzle and solve"""
    filename = "./python/2023/input/15.txt"
    lines = []
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readline().split(",")

    boxes = defaultdict(list)

    for line in lines:
        label = None
        box = None
        focal = None
        if "=" in line:
            """
            If the operation character is an equals sign (=), it will be followed by a number
            indicating the focal length of the lens that needs to go into the relevant box; be
            sure to use the label maker to mark the lens with the label given in the beginning
            of the step so you can find it later. There are two possible situations:

            If there is already a lens in the box with the same label, replace the old lens with
            the new lens: remove the old lens and put the new lens in its place, not moving any
            other lenses in the box.
            
            If there is not already a lens in the box with the same label, add the lens to the
            box immediately behind any lenses already in the box. Don't move any of the other
            lenses when you do this. If there aren't any lenses in the box, the new lens goes
            the way to the front of the box.

            """
            label, focal = line.split("=")
            box = hash(label.strip())
            focal = int(focal.strip())
            lens = (label, focal)
            replaced = False
            for idx, lenses in enumerate(boxes[box]):
                if lenses[0] == label:
                    boxes[box][idx] = lens
                    replaced = True
                    break
            if not replaced:
                boxes[box].append(lens)
        else:
            """
            If the operation character is a dash (-), go to the relevant box and remove the lens
            with the given label if it is present in the box. Then, move any remaining lenses as
            far forward in the box as they can go without changing their order, filling any space made by
            removing the indicated lens.
            
            (If no lens in that box has the given label, nothing happens.)
            """
            label = line.strip().split("-")[0]
            box = hash(label)
            for idx, lenses in enumerate(boxes[box]):
                if lenses[0] == label:
                    boxes[box].pop(idx)
                    break


    focusing_power = 0
    for box_id, box in boxes.items():
        for idx, lens in enumerate(box):
            focusing_power += (box_id + 1) * (idx + 1) * lens[1]

    print_solution(focusing_power)


if __name__ == "__main__":
    main()
