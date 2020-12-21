from collections import defaultdict


def printSolution(x):
    print(f"The solution is: {x}")


class Food:
    def __init__(self):
        self.id = None
        self.ingredients = []
        self.allergens = []
        self.warnings = []

    def __repr__(self):
        return f"Food: id:{self.id}, ingredients:{self.ingredients}, allergens:{self.allergens}, warning:{self.warning}"


def main():

    foods = []
    allergens = defaultdict(set)
    inert = set()

    f = Food()
    file = open("input.txt", "r")
    for idx, line in enumerate(file):
        food_i, food_a = line.strip().split("(contains ")
        food_i = food_i.split()
        food_a = food_a.strip(")").split(", ")

        f.id = idx
        f.ingredients = food_i
        f.warnings = food_a

        inert.update(set(food_i))

        for a in food_a:
            if len(allergens[a]):
                allergens[a] = allergens[a].intersection(food_i)
            else:
                allergens[a] = set(food_i)

        foods.append(f)
        f = Food()

    for bad_ingredients in allergens.values():
        inert.difference_update(bad_ingredients)

    while not all([len(x) == 1 for x in allergens.values()]):
        for k, v in allergens.items():
            if len(v) == 1:
                isolated = list(v)[0]
                for aller in allergens:
                    if aller != k and isolated in allergens[aller]:
                        allergens[aller].remove(isolated)

    sorted_allergens = sorted(list(allergens.keys()))
    dangerous = [list(allergens[x])[0] for x in sorted_allergens]
    printSolution(','.join(dangerous))


if __name__ == "__main__":
    main()
