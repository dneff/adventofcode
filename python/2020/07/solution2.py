from collections import defaultdict


def printSolution(x):
    print(f"The solution is: {x}")


class Rules:
    def __init__(self, rules_list):
        self.rules = self.createRulesGraph(rules_list)

    def __len__(self):
        return len(self.rules.keys())

    def containedBagCount(self, bag):
        # gets count of required sub-bags
        count = len(self.rules[bag])
        if count != 0:
            for b in self.rules[bag]:
                count += self.containedBagCount(b)
        return count

    def bagsContaining(self, test_bag):
        # gets count of bags containing test_bag
        is_valid = [self.canContain(r, test_bag) for r in self.rules.keys()]
        return is_valid.count(True)

    def canContain(self, bag, test_bag):
        # checks if test_bag can be at any depth in bag
        to_check = list(set(self.rules[bag][:]))
        if test_bag in to_check:
            return True

        checked = []
        while to_check:
            b = to_check.pop(0)
            if b in checked:
                continue
            else:
                checked.append(b)
                if test_bag in self.rules[b]:
                    return True
                else:
                    to_check.extend(self.rules[b])
        return False

    def createRulesGraph(self, rule_list):
        # generates rules graph
        rules = defaultdict(list)

        for rule in rule_list:
            r = rule.split(" bags contain ")
            for b in r[1].split(", "):
                if b[:2] != "no":
                    count = int(b[0])
                    bag = " ".join(b.split(" ")[1:3])
                    rules[r[0]].extend([bag] * count)
                else:
                    rules[r[0]] = []

        return rules


def main():

    file = open("input.txt", "r")
    rule_data = [line.strip() for line in file.readlines()]

    rules = Rules(rule_data)
    test_bag = "shiny gold"

    printSolution(rules.containedBagCount(test_bag))


if __name__ == "__main__":
    main()