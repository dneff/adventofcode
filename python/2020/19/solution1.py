def printSolution(x):
    print(f"The solution is: {x}")


class Reader:
    def __init__(self):
        self.rules = {}
        self.resolved = {}

    def load(self, rule_data):
        for rule in rule_data:
            k, v = rule.split(": ")
            k = int(k)
            if v[0] == '"':
                r = v.replace('"', "")
                self.resolved[k] = {r}
            elif "|" in v:
                r = v.split(" | ")
                r = set(map(lambda x: tuple(map(int, x.split())), r))
            else:
                r = tuple(map(int, v.split()))
            self.rules[k] = r

    def resolve(self, rule_id):
        if rule_id not in self.resolved:
            rule = self.rules[rule_id]
            if type(rule) == str:
                res = {rule}
            elif type(rule) == tuple:
                if len(rule) == 1:
                    res = self.resolve(rule[0])
                else:
                    res = set()
                    r1, r2 = rule
                    for x in self.resolve(r1):
                        for y in self.resolve(r2):
                            res.add(x + y)
            else:
                r1, r2 = tuple(rule)
                if len(r1) == 1:
                    res = self.resolve(r1[0]) | self.resolve(r2[0])
                else:
                    res = set()
                    for x in self.resolve(r1[0]):
                        for y in self.resolve(r1[1]):
                            res.add(x + y)

                    alt = set()
                    for x in self.resolve(r2[0]):
                        for y in self.resolve(r2[1]):
                            alt.add(x + y)

                    res |= alt
            self.resolved[rule_id] = res

        return self.resolved[rule_id]

    def valid(self, message, rule_id):
        if rule_id not in self.resolved:
            self.resolve(rule_id)
        return message in self.resolved[rule_id]


def main():
    file = open("input.txt", "r")

    reader = Reader()

    rule_data = []
    messages = []

    for line in file:
        line = line.strip()
        if not line:
            continue
        if line[0].isdigit():
            rule_data.append(line)
        else:
            messages.append(line)

    reader.load(rule_data)

    valid = [reader.valid(message, 0) for message in messages]

    printSolution(sum(valid))


if __name__ == "__main__":
    main()
