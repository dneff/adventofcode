# very challenging to reason through
# solution from github: jcisio/adventofcode2019

import math

def oreNeeded(materials, reactions, distance, fuel):
    needed = {'FUEL': fuel}
    while len(needed) > 1 or 'ORE' not in needed:
        material = max(needed, key=lambda x: distance[x])
        quantity = needed[material]
        del needed[material]
        base_quantity, ingredients = reactions[material].values()
        for a, b in ingredients.items():
            if a not in needed:
                needed[a] = 0
            needed[a] += math.ceil(quantity/base_quantity) * b
    return needed['ORE']

def main():

    reactions = {}
    materials = {'ORE'}
    distance = {'ORE': 0}

    with open('input1.txt', 'r') as file:
        for data in file.readlines():
            l, r = data.strip().split(' => ')
            output = r.split()
            reactions[output[1]] = {
                'qty': int(output[0]),
                'ingredients': {i[1]: int(i[0]) for i in [i.split() for i in l.split(', ')]}
            }
            materials.add(output[1])

    while len(distance) < len(materials):
        for material in materials:
            if material in distance:
                continue
            if not all([i in distance for i in reactions[material]['ingredients'].keys()]):
                continue
            distance[material] = max([distance[i] for i in reactions[material]['ingredients'].keys()]) + 1

    sol1 = oreNeeded(materials, reactions, distance, 1)

    print(f"Solution 1: One fuel requires {sol1} ore.")

# Part 2 -=-=-=-

    capacity = 1000000000000

    target = capacity//sol1
    used_ore = oreNeeded(materials, reactions, distance, target)
    while True:
        target += (capacity - used_ore)//sol1 + 1
        used_ore = oreNeeded(materials, reactions, distance, target)
        if used_ore > capacity:
            break

    print(f"Solution 2: Given 1 trillion ore, the maximum amount of fuel produced is {target - 1}")

if __name__ == "__main__":
    main()