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
            elif "|" in v:
                r = v.split(" | ")
                r = frozenset(map(lambda x: tuple(map(int, x.split())), r))
            else:
                r = tuple(map(int, v.split()))
            self.rules[k] = r

    def resolve(self, message, rule):
        if (message, rule) not in self.resolved:
            if rule == frozenset({(42,), (42, 8)}):
                if len(message) % 8:
                    res = False
                else:
                    res = True
                    for i in range(0, len(message), 8):
                        if not self.resolve(message[i : i + 8], self.rules[42]):
                            res = False
                            break
            elif rule == frozenset({(42, 31), (42, 11, 31)}):
                if len(message) % 8:
                    res = False
                else:
                    res = True
                    for i in range(0, len(message) // 2, 8):
                        if not self.resolve(message[i : i + 8], self.rules[42]):
                            res = False
                            break
                    if res:
                        for i in range(len(message) // 2, len(message), 8):
                            if not self.resolve(message[i : i + 8], self.rules[31]):
                                res = False
                                break
            else:
                if type(rule) == str:
                    res = message == rule
                elif type(rule) == tuple:
                    if len(rule) == 1:
                        res = self.resolve(message, self.rules[rule[0]])
                    else:
                        res = False
                        r1, r2 = self.rules[rule[0]], self.rules[rule[1]]
                        for i in range(1, len(message)):
                            if self.resolve(message[:i], r1) and self.resolve(
                                message[i:], r2
                            ):
                                res = True
                                break
                else:
                    res = False
                    for r in rule:
                        if self.resolve(message, r):
                            res = True
                            break

            self.resolved[message, rule] = res

        return self.resolved[message, rule]

    def valid(self, message, rule):
        if (message, rule) not in self.resolved:
            self.resolve(message, rule)
        return self.resolved[message, rule]


def main():
    file = open("input2.txt", "r")

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

    valid = [reader.valid(message, reader.rules[0]) for message in messages]

    printSolution(sum(valid))


if __name__ == "__main__":
    main()
