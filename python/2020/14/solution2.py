import re


def printSolution(x):
    print(f"The solution is: {x}")


class Docker:
    def __init__(self):
        self.mask = {}
        self.memory = {}

    def createMask(self, mask_data):
        self.mask.clear()
        for idx, i in enumerate(range(len(mask_data))):
            if mask_data[i] == "X":
                self.mask[idx] = mask_data[i]
            else:
                self.mask[idx] = mask_data[i]

    def fuzzToMemory(self, fuzzed):
        if "X" not in fuzzed:
            return [int(fuzzed, 2)]

        i = fuzzed.find("X")

        return self.fuzzToMemory(
            fuzzed[:i] + "0" + fuzzed[i + 1 :]
        ) + self.fuzzToMemory(fuzzed[:i] + "1" + fuzzed[i + 1 :])

    def put(self, mem_location, value):
        bin_mem = [x for x in bin(mem_location)[2:]]
        if len(bin_mem) < max(self.mask.keys()):
            bin_mem = ["0"] * (max(self.mask.keys()) - len(bin_mem) + 1) + bin_mem

        fuzz = ""
        for idx, mem in enumerate(bin_mem):
            if idx in self.mask.keys():
                if self.mask[idx] in ["X", "1"]:
                    fuzz += self.mask[idx]
                else:
                    fuzz += mem
            else:
                fuzz += mem

        for mem in self.fuzzToMemory(fuzz):
            self.memory[mem] = value

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
