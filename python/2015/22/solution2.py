import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2015/22/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils
import copy


spells = {}
spells['missle'] = {'name': 'missle', 'cost': 53, 'attack': 4, 'armor': 0, 'heal': 0, 'mana': 0, 'turns': 0}
spells['drain'] = {'name': 'drain', 'cost': 73, 'attack': 2, 'armor': 0, 'heal': 2, 'mana': 0, 'turns': 0}
spells['shield'] = {'name': 'shield', 'cost': 113, 'attack': 0, 'armor': 7, 'heal': 0, 'mana': 0, 'turns': 6}
spells['poison'] = {'name': 'poison', 'cost': 173, 'attack': 3, 'armor': 0, 'heal': 0, 'mana': 0, 'turns': 6}
spells['recharge'] = {'name': 'recharge', 'cost': 229, 'attack': 0, 'armor': 0, 'heal': 0, 'mana': 101, 'turns': 5}

minimum_mana = 100 ** 15

class Wizard():
    def __init__(self, hp, mana):
        self.hp = hp
        self.mana = mana
        self.attack = 1
        self.armor = 0
        self.effects = []
        self.mana_used = 0

def resolveTurn(player, boss, spell):
    global minimum_mana, spells
    ''' starts as player casts spell '''
    if player.mana_used > minimum_mana:
        return player.mana_used
    # cast spell
    player.mana -= spell['cost']
    player.mana_used += spell['cost']
    if spell['turns'] > 0:
        player.effects.append(copy.deepcopy(spell))
    else:
        boss.hp -= spell['attack']
        player.hp += spell['heal']
    if boss.hp < 0:
        return player.mana_used

    # begin boss turn
    player.armor = 0
    # - resolve effects
    ending = []
    for idx, spell in enumerate(player.effects):
        boss.hp -= spell['attack']
        player.mana += spell['mana']
        player.armor += spell['armor']
        player.effects[idx]['turns'] -= 1
        if player.effects[idx]['turns'] == 0:
            ending.append(idx)

    ending.sort(reverse=True)
    for i in ending:
        player.effects.pop(i)

    if boss.hp < 0:
        return player.mana_used

    # - boss attack
    player.hp -= max(1, boss.attack - player.armor)

    if player.hp <= 0:
        return minimum_mana

    # begin player turn
    player.hp -= 1
    if player.hp <= 0:
        return minimum_mana

    # - resolve effects
    ending = []
    for idx, spell in enumerate(player.effects):
        boss.hp -= spell['attack']
        player.mana += spell['mana']
        player.armor += spell['armor']
        player.effects[idx]['turns'] -= 1
        if player.effects[idx]['turns'] == 0:
            ending.append(idx)

    ending.sort(reverse=True)
    for i in ending:
        player.effects.pop(i)

    if boss.hp < 0:
        return player.mana_used

    # - resolveTurn()
    invalid_spells = [spell['name'] for spell in player.effects]
    costs = [minimum_mana]
    for spell in spells.values():
        if spell['name'] in invalid_spells:
            continue
        if spell['cost'] <= player.mana:
            result = resolveTurn(copy.deepcopy(player), copy.deepcopy(boss), spell)
            if type(result) == int:
                costs.append(result)
    minimum_mana = min(costs)
    return min(costs)


def solve_part2():
    global minimum_mana
    player = Wizard(50, 500)
    boss = Wizard(55, 0)
    boss.attack = 8

    player.hp -= 1

    for spell in spells.values():
        result = resolveTurn(copy.deepcopy(player), copy.deepcopy(boss), spell)
        if type(result) == int:
            minimum_mana = min(minimum_mana, result)

    return minimum_mana

answer = solve_part2()
AoCUtils.print_solution(2, answer)
