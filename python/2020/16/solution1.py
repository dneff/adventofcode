from collections import defaultdict


def printSolution(x):
    print(f"The solution is: {x}")


class Validator:
    def __init__(self, limit_data):
        self.limits = defaultdict(set)
        for limit in limit_data:
            k, v = limit.split(": ")
            ranges = v.split(" or ")
            for r in ranges:
                lo, hi = [int(x) for x in r.split("-")]
                self.limits[k] = self.limits[k].union(range(lo, hi + 1))

    def check(self, ticket):
        result = []
        for val in ticket:
            valid = False
            for r in self.limits.values():
                if val in r:
                    valid = True
                    break
            if not valid:
                result.append(val)
        return result


def main():
    file = open("input.txt", "r")

    sections = defaultdict(list)
    part = 0
    for line in file:
        if line.strip():
            sections[part].append(line.strip())
        else:
            part += 1

    rules = sections[0]
    my_ticket = [int(x) for x in sections[1][1].split(",")]
    other_tickets = []
    for t in sections[2][2:]:
        other_tickets.append([int(x) for x in t.split(",")])

    ticket_checker = Validator(rules)

    invalid = []
    for t in other_tickets:
        invalid.extend(ticket_checker.check(t))

    printSolution(sum(invalid))


if __name__ == "__main__":
    main()
