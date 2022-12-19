import string


def printSolution(x):
    print(f"The solution is: {x}")


class Passport:
    def __init__(self):
        self.valid = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]

    def addField(self, field, value):
        self.__dict__[field] = value

    def isValid(self):
        # checks all fields exist
        for field in self.valid:
            if not hasattr(self, field):
                return False
        if not 1920 <= int(self.byr) <= 2002:
            return False
        if not 2010 <= int(self.iyr) <= 2020:
            return False
        if not 2020 <= int(self.eyr) <= 2030:
            return False
        h, m = int(self.hgt[:-2]), self.hgt[-2:]
        if m == "cm":
            if not 150 <= h <= 193:
                return False
        else:
            if not 59 <= h <= 76:
                return False

        if not self.hcl[0] == "#":
            return False

        if not all(x in string.hexdigits for x in self.hcl[1:]):
            return False

        if self.ecl not in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
            return False

        if not (len(self.pid) == 9 and self.pid.isdigit()):
            return False

        return True

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


def main():

    file = open("input.txt", "r")

    credentials = []

    # generate list of credentials
    cred = Passport()
    for line in file:
        if line.strip():
            for kv in line.strip().split(" "):
                k, v = kv.split(":")
                cred.addField(k, v)
        else:
            # new line! save this cred and start a new one
            credentials.append(cred)
            cred = Passport()
    # finish last cred
    credentials.append(cred)

    valid_count = sum([c.isValid() for c in credentials])
    printSolution(valid_count)


if __name__ == "__main__":
    main()