import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCUtils  # noqa: E402
from collections import defaultdict  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2015/21/input')


item_shop = {}

item_shop["weapons"] = {}
item_shop["weapons"]["dagger"] = {"cost": 8, "attack": 4, "armor": 0}
item_shop["weapons"]["shortsword"] = {"cost": 10, "attack": 5, "armor": 0}
item_shop["weapons"]["warhammer"] = {"cost": 25, "attack": 6, "armor": 0}
item_shop["weapons"]["longsword"] = {"cost": 40, "attack": 7, "armor": 0}
item_shop["weapons"]["greataxe"] = {"cost": 74, "attack": 8, "armor": 0}

item_shop["armors"] = {}
item_shop["armors"]["none"] = {"cost": 0, "attack": 0, "armor": 0}
item_shop["armors"]["leather"] = {"cost": 13, "attack": 0, "armor": 1}
item_shop["armors"]["chainmail"] = {"cost": 31, "attack": 0, "armor": 2}
item_shop["armors"]["splintmail"] = {"cost": 53, "attack": 0, "armor": 3}
item_shop["armors"]["bandedmail"] = {"cost": 75, "attack": 0, "armor": 4}
item_shop["armors"]["platemail"] = {"cost": 102, "attack": 0, "armor": 5}

item_shop["rings"] = {}
item_shop["rings"]["none"] = {"cost": 0, "attack": 0, "armor": 0}
item_shop["rings"]["dmg_1"] = {"cost": 25, "attack": 1, "armor": 0}
item_shop["rings"]["dmg_2"] = {"cost": 50, "attack": 2, "armor": 0}
item_shop["rings"]["dmg_3"] = {"cost": 100, "attack": 3, "armor": 0}
item_shop["rings"]["def_1"] = {"cost": 20, "attack": 0, "armor": 1}
item_shop["rings"]["def_2"] = {"cost": 40, "attack": 0, "armor": 2}
item_shop["rings"]["def_3"] = {"cost": 80, "attack": 0, "armor": 3}


class Fighter:
    def __init__(self):
        self.hp = 0
        self.attack = 1
        self.armor = 0
        self.cost = 0

    def fight(self, monster):
        my_hp = self.hp
        their_hp = monster.hp
        while my_hp > 0:
            their_hp -= max(1, self.attack - monster.armor)
            if their_hp <= 0:
                return True
            my_hp -= max(1, monster.attack - self.armor)
        return False

    def equip(self, cost, attack, armor):
        self.cost = cost
        self.attack = attack
        self.armor = armor


def getMostExpensiveOutfit():
    outfits = defaultdict(list)
    for weapon in item_shop["weapons"]:
        for armor in item_shop["armors"]:
            for r1 in item_shop["rings"]:
                for r2 in item_shop["rings"]:
                    if r1 == r2 and r1 != "none":
                        continue
                    outfit_cost = (
                        item_shop["weapons"][weapon]["cost"]
                        + item_shop["armors"][armor]["cost"]
                        + item_shop["rings"][r1]["cost"]
                        + item_shop["rings"][r2]["cost"]
                    )

                    outfit_attack = (
                        item_shop["weapons"][weapon]["attack"]
                        + item_shop["armors"][armor]["attack"]
                        + item_shop["rings"][r1]["attack"]
                        + item_shop["rings"][r2]["attack"]
                    )

                    outfit_armor = (
                        item_shop["weapons"][weapon]["armor"]
                        + item_shop["armors"][armor]["armor"]
                        + item_shop["rings"][r1]["armor"]
                        + item_shop["rings"][r2]["armor"]
                    )
                    outfits[outfit_cost].append((outfit_attack, outfit_armor))
    prices = list(outfits.keys())
    prices.sort(reverse=True)

    for p in prices:
        for outfit in outfits[p]:
            yield (p, outfit[0], outfit[1])


def solve_part2():

    player = Fighter()
    player.hp = 100

    boss = Fighter()
    boss.hp = 104
    boss.attack = 8
    boss.armor = 1

    outfits = getMostExpensiveOutfit()

    player.equip(*next(outfits))
    while player.fight(boss):
        player.equip(*next(outfits))
    return player.cost


answer = solve_part2()
AoCUtils.print_solution(2, answer)
