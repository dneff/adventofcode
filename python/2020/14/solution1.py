import re


def printSolution(x):
    print(f"The solution is: {x}")


class Docker:
    def __init__(self):
        self.mask = {}
        self.memory = {}

    def createMask(self, mask_data):
        self.mask.clear()
        for idx, i in enumerate(range(len(mask_data) - 1, -1, -1)):
            if mask_data[i] == "X":
                continue
            else:
                self.mask[idx] = int(mask_data[i])


    def put(self, mem_location, value):
        bin_val = [int(x) for x in bin(value)[2:]]
        if len(bin_val) < max(self.mask.keys()):
            bin_val = [0] * (max(self.mask.keys()) - len(bin_val) + 1) + bin_val
        for p, v in self.mask.items():
            # indexing from right to left, so starting val is -1
            bin_val[-p - 1] = v

        f_val = int("".join([str(x) for x in bin_val]), 2)

        self.memory[mem_location] = f_val

    def getMemorySum(self):
        return sum(self.memory.values())


def main():
    file = open("input.txt", "r")

    d = Docker()
    for line in file:
        k, v = line.strip().split(" = ")
        if k == "mask":
            d.createMask(v)
        if k[:3] == "mem":
            mem_loc = int(re.findall("\d+", k)[0])
            d.put(mem_loc, int(v))

    printSolution(d.getMemorySum())



if __name__ == "__main__":
    main()