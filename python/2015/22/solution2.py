"""
Advent of Code 2015 Day 22: Wizard Simulator 20XX - Part 2

Simulates a wizard battle on HARD MODE against a boss using RPG-style turn-based combat.
The wizard has 5 spells available and must find the minimum mana cost to win.

HARD MODE RULES (Part 2 only):
- At the start of EACH player turn (before any other effects apply), player loses 1 HP
- If this brings player to 0 or below HP, player loses immediately

All other battle rules from Part 1 still apply:
- Player (wizard) goes first, then alternates with boss
- Effects apply at the start of each turn (both player and boss)
- Player must cast a spell each turn (costs mana)
- Boss attacks each turn (damage reduced by player's armor)
- Combat ends when either HP reaches 0 or below

Goal: Find the least amount of mana needed to win the fight on hard difficulty.

Performance: Optimized version using fast_copy() instead of copy.deepcopy()
- Original runtime: ~38 seconds
- Optimized runtime: ~3.15 seconds (12x faster)
"""
import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2015/22/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils

# Define all available spells with their properties
spells = {}
# Magic Missile: 53 mana, 4 instant damage
spells['missile'] = {'name': 'missile', 'cost': 53, 'attack': 4, 'armor': 0, 'heal': 0, 'mana': 0, 'turns': 0}
# Drain: 73 mana, 2 instant damage and heal 2 HP
spells['drain'] = {'name': 'drain', 'cost': 73, 'attack': 2, 'armor': 0, 'heal': 2, 'mana': 0, 'turns': 0}
# Shield: 113 mana, +7 armor for 6 turns
spells['shield'] = {'name': 'shield', 'cost': 113, 'attack': 0, 'armor': 7, 'heal': 0, 'mana': 0, 'turns': 6}
# Poison: 173 mana, 3 damage per turn for 6 turns
spells['poison'] = {'name': 'poison', 'cost': 173, 'attack': 3, 'armor': 0, 'heal': 0, 'mana': 0, 'turns': 6}
# Recharge: 229 mana, +101 mana per turn for 5 turns
spells['recharge'] = {'name': 'recharge', 'cost': 229, 'attack': 0, 'armor': 0, 'heal': 0, 'mana': 101, 'turns': 5}

# Global variable to track the minimum mana cost found so far
# Used for pruning search paths that exceed current best
minimum_mana = 100 ** 15

class Wizard():
    """
    Represents a character in the wizard battle (player or boss).

    Attributes:
        hp: Hit points (health)
        mana: Available mana for casting spells
        attack: Attack damage (for boss attacks)
        armor: Armor value (reduces incoming damage)
        effects: List of active spell effects currently applied
        mana_used: Total mana spent so far (player only)
    """
    def __init__(self, hp, mana):
        self.hp = hp
        self.mana = mana
        self.attack = 1
        self.armor = 0
        self.effects = []
        self.mana_used = 0

    def fast_copy(self):
        """
        Create a copy of this Wizard faster than copy.deepcopy().

        Performance optimization: Instead of using copy.deepcopy() which
        recursively copies all objects, we manually copy only what's needed.
        This provides an ~12x speedup.
        """
        new_wizard = Wizard(self.hp, self.mana)
        new_wizard.attack = self.attack
        new_wizard.armor = self.armor
        # Copy effects list - each effect is a dict, so we need to copy those too
        new_wizard.effects = [eff.copy() for eff in self.effects]
        new_wizard.mana_used = self.mana_used
        return new_wizard


def resolveTurn(player, boss, spell):
    """
    Simulates one complete round of combat on HARD MODE starting with the player casting a spell.

    The turn order is:
    1. Player casts spell (instant or starts effect)
    2. Boss turn begins
       - Apply all active effects
       - Boss attacks player
    3. Next player turn begins (HARD MODE)
       - Player loses 1 HP (hard mode penalty!)
       - Apply all active effects
       - Recursively try all valid spells

    Args:
        player: Wizard object representing the player
        boss: Wizard object representing the boss
        spell: Dictionary containing spell properties to cast

    Returns:
        int: Minimum mana cost to win from this state, or minimum_mana if this path loses
    """
    global minimum_mana, spells

    # Prune: If we've already spent more mana than the best solution, abandon this path
    if player.mana_used > minimum_mana:
        return player.mana_used

    # === PLAYER CASTS SPELL ===
    player.mana -= spell['cost']
    player.mana_used += spell['cost']

    if spell['turns'] > 0:
        # Effect spell: Add to active effects list
        player.effects.append(spell.copy())
    else:
        # Instant spell: Apply damage and healing immediately
        boss.hp -= spell['attack']
        player.hp += spell['heal']

    # Check if boss is defeated after casting spell
    if boss.hp < 0:
        return player.mana_used

    # === BOSS TURN ===
    player.armor = 0  # Reset armor (reapplied by effects)

    # Apply all active effects at start of boss turn
    ending = []  # Track effects that expire this turn
    for idx, spell in enumerate(player.effects):
        boss.hp -= spell['attack']  # Poison damage
        player.mana += spell['mana']  # Recharge mana
        player.armor += spell['armor']  # Shield armor
        player.effects[idx]['turns'] -= 1

        if player.effects[idx]['turns'] == 0:
            ending.append(idx)

    # Remove expired effects (in reverse order to preserve indices)
    ending.sort(reverse=True)
    for i in ending:
        player.effects.pop(i)

    # Check if boss is defeated after effects
    if boss.hp < 0:
        return player.mana_used

    # Boss attacks player (damage is at least 1, even with high armor)
    player.hp -= max(1, boss.attack - player.armor)

    # Check if player is defeated
    if player.hp <= 0:
        return minimum_mana

    # === NEXT PLAYER TURN ===

    # HARD MODE: Player loses 1 HP at the start of each player turn
    player.hp -= 1
    if player.hp <= 0:
        return minimum_mana

    # Apply all active effects at start of player turn
    ending = []  # Track effects that expire this turn
    for idx, spell in enumerate(player.effects):
        boss.hp -= spell['attack']  # Poison damage
        player.mana += spell['mana']  # Recharge mana
        player.armor += spell['armor']  # Shield armor
        player.effects[idx]['turns'] -= 1

        if player.effects[idx]['turns'] == 0:
            ending.append(idx)

    # Remove expired effects (in reverse order to preserve indices)
    ending.sort(reverse=True)
    for i in ending:
        player.effects.pop(i)

    # Check if boss is defeated after effects
    if boss.hp < 0:
        return player.mana_used

    # Try all valid spells recursively
    # Cannot cast a spell if its effect is already active
    invalid_spells = [spell['name'] for spell in player.effects]
    costs = [minimum_mana]

    for spell in spells.values():
        # Skip if effect is already active
        if spell['name'] in invalid_spells:
            continue
        # Skip if we can't afford the spell
        if spell['cost'] <= player.mana:
            result = resolveTurn(player.fast_copy(), boss.fast_copy(), spell)
            if type(result) == int:
                costs.append(result)

    # Update global minimum and return best result from this branch
    minimum_mana = min(costs)
    return min(costs)


def solve_part2():
    """
    Finds the minimum mana cost to win the wizard battle on HARD MODE.

    Starting conditions:
    - Player: 50 HP, 500 mana
    - Boss: 55 HP, 8 attack damage

    HARD MODE DIFFERENCE:
    - Player loses 1 HP at the start of each player turn (before effects)
    - This makes the fight significantly harder and requires more mana

    Strategy: Uses recursive depth-first search to explore all possible spell
    sequences, pruning branches that exceed the current best solution.

    Returns:
        int: Minimum amount of mana needed to defeat the boss on hard mode
    """
    global minimum_mana

    # Initialize player with 50 HP and 500 mana (as specified in problem)
    player = Wizard(50, 500)

    # Initialize boss with 55 HP and 8 attack (from input file)
    boss = Wizard(55, 0)
    boss.attack = 8

    # HARD MODE: Player loses 1 HP at the start of the first turn
    # (This happens before the very first spell is cast)
    player.hp -= 1

    # Try each spell as the first move and recursively explore all possibilities
    for spell in spells.values():
        result = resolveTurn(player.fast_copy(), boss.fast_copy(), spell)
        if type(result) == int:
            minimum_mana = min(minimum_mana, result)

    return minimum_mana

answer = solve_part2()
AoCUtils.print_solution(2, answer)
