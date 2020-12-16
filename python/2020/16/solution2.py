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

    def check_ticket(self, ticket):
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

    def valid_fields(self, values):
        valid = []
        for k, v in self.limits.items():
            if set(values).issubset(v):
                valid.append(k)
        return valid


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
    for t in sections[2][1:]:
        other_tickets.append([int(x) for x in t.split(",")])

    ticket_checker = Validator(rules)

    valid = []
    for t in other_tickets:
        if not ticket_checker.check_ticket(t):
            valid.append(t)

    val_by_field = []
    for idx in range(len(valid[0])):
        val_by_field.append(list(zip(*valid))[idx])

    fields = [False] * len(val_by_field)

    while not all(fields):
        for idx, vals in enumerate(val_by_field):
            possible = [x for x in ticket_checker.valid_fields(vals) if x not in fields]
            if len(possible) == 1:
                fields[idx] = possible[0]

    departure_product = 1
    for idx, name in enumerate(fields):
        if name.startswith("departure"):
            departure_product *= my_ticket[idx]

    printSolution(departure_product)


if __name__ == "__main__":
    main()
