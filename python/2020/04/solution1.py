def printSolution(x):
    print(f"The solution is: {x}")

class Passport():
    def __init__(self, valid = []):
        self.valid = valid[:]

    def addField(self, field, value):
        self.__dict__[field] = value

    def setValid(self, fieldNames):
        self.valid = fieldNames[:]

    def isValid(self):
        for key in self.valid:
            if not hasattr(self, key):
                return False
        return True
    
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)    

def main():

    file = open('input.txt', 'r')

    credentials = []
    valid_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

    # generate list of credentials
    cred = Passport(valid_fields)
    for line in file:
        if line.strip():
            for kv in line.strip().split(" "):
                k,v = kv.split(':')
                cred.addField(k,v)
        else:
            # new line! save this cred and start a new one
            credentials.append(cred)
            cred = Passport(valid_fields)
    # finish last cred
    credentials.append(cred)

    valid_count = sum([c.isValid() for c in credentials])
    printSolution(valid_count)


if __name__ == "__main__":
    main()