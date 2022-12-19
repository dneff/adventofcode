from collections import deque
import math


def printSolution(x):
    print(f"The solution is {x}")


class Radio:
    def __init__(self):
        self.received = deque()
        self.buffer = ''
        self.bit_counter = 0
        self.version_counter = 0
        self.packet_bitcounts = []
        self.message_value = 0

    def getBitCount(self):
        return self.bit_counter - len(self.buffer)

    def hex2bin(self, x):
        return bin(int(str(x), 16))[2:].zfill(4)

    def __extendBuffer(self):
        buffer_start = len(self.buffer)
        self.buffer += self.hex2bin(self.received.popleft())
        self.bit_counter += len(self.buffer) - buffer_start

    def get(self, x):
        while x > len(self.buffer):
            self.__extendBuffer()
        result, self.buffer = self.buffer[:x], self.buffer[x:]
        return result

    def getPacket(self):
        version = int(self.get(3), 2)
        type_id = int(self.get(3), 2)
        self.version_counter += version

        operator = []
        if type_id != 4:

            length_type = int(self.get(1), 2)
            if length_type == 0:
                # total length
                packet_length = int(self.get(15), 2)
                if packet_length > 0:
                    bits = self.getBitCount()
                    while packet_length > self.getBitCount() - bits:
                        operator.append(self.getPacket())
            else:
                # number of sub-packets
                packet_count = int(self.get(11), 2)
                for p in range(packet_count):
                    operator.append(self.getPacket())

        if type_id == 0:
            return sum(operator)
        elif type_id == 1:
            return math.prod(operator)
        elif type_id == 2:
            return min(operator)
        elif type_id == 3:
            return max(operator)
        elif type_id == 4:
            literal = ''
            parsing = True
            while parsing:
                group = self.get(5)
                literal += group[1:]
                if group[0] == '0':
                    parsing = False
            return int(literal, 2)
        elif type_id == 5:
            greater = operator[0] > operator[1]
            if greater:
                return 1
            else:
                return 0
        elif type_id == 6:
            lesser = operator[0] < operator[1]
            if lesser:
                return 1
            else:
                return 0
        elif type_id == 7:
            equal = operator[0] == operator[1]
            if equal:
                return 1
            else:
                return 0


def main():
    test = 'test.txt'
    puzzle = 'input.txt'

    file = open(puzzle, 'r')
    for line in file.readlines():
        transmission = list(line.strip())
        r = Radio()
        r.received.extend(transmission)
        r.getPacket()
        printSolution(r.version_counter)
        r.received.clear()
        r.buffer = ''


if __name__ == "__main__":
    main()
