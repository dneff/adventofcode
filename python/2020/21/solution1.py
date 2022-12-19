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
    ingredients = set()

    f = Food()
    file = open("input.txt", "r")
    for idx, line in enumerate(file):
        food_i, food_a = line.strip().split("(contains ")
        food_i = food_i.split()
        food_a = food_a.strip(")").split(", ")

        f.id = idx
        f.ingredients = food_i
        f.warnings = food_a

        ingredients.update(set(food_i))

        for a in food_a:
            if len(allergens[a]):
                allergens[a] = allergens[a].intersection(food_i)
            else:
                allergens[a] = set(food_i)

        foods.append(f)
        f = Food()

    for bad_ingredients in allergens.values():
        ingredients.difference_update(bad_ingredients)

    used = 0
    for f in foods:
        used += len(ingredients.intersection(set(f.ingredients)))

    printSolution(used)


if __name__ == "__main__":
    main()
