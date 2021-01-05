import string


def printSolution(x):
    print(f"The solution is: {x}")


class PasswordManager:
    def __init__(self):
        self.password = []

    def add(self, pwd):
        self.password = pwd

    def hasPair(self, s):
        for i, x in enumerate(s[:-1]):
            if x == s[i + 1]:
                return True
        return False

    def verify(self, s):
        # must not contain i, o, l
        for invalid in ["i", "o", "l"]:
            if invalid in s:
                return False

        # must contain two non-overlapping pairs
        pairs = False
        for i, x in enumerate(s[:-1]):
            if x == s[i + 1]:
                if self.hasPair(s[i + 2:]):
                    pairs = True
                    break
        if not pairs:
            return False

        # must contain straight of at least three letters
        triplets = False
        for i, l in enumerate(s[:-2]):
            letter_pos = string.ascii_lowercase.find(l)
            test_triplet = string.ascii_lowercase[letter_pos: letter_pos + 3]
            if len(test_triplet) != 3:
                continue
            if test_triplet in s:
                triplets = True
                break

        return triplets

    def increment(self, s):
        iterator = [string.ascii_lowercase.find(x) for x in s]
        iterator[-1] += 1

        for i in range(len(iterator) - 1, 0, -1):
            iterator[i - 1] += iterator[i] // len(string.ascii_lowercase)
            iterator[i] %= len(string.ascii_lowercase)
        iterator[0] %= len(string.ascii_lowercase)

        return "".join([string.ascii_lowercase[x] for x in iterator])

    def next(self):
        possible = self.increment(self.password)
        while not self.verify(possible):
            possible = self.increment(possible)
        self.password = possible


def main():
    input = "hepxcrrq"

    pm = PasswordManager()
    pm.add(input)
    pm.next()
    printSolution(pm.password)


if __name__ == "__main__":
    main()
