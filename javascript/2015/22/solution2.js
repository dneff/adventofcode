/**
 * Advent of Code 2015 - Day 22: Wizard Simulator 20XX - Part 2
 * https://adventofcode.com/2015/day/22
 *
 * Simulates a wizard battle on HARD MODE against a boss.
 * In hard mode, player loses 1 HP at the start of each player turn.
 */

import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const INPUT_FILE = join(__dirname, '../../../aoc-data/2015/22/input');

const spells = {
  missile: { name: 'missile', cost: 53, attack: 4, armor: 0, heal: 0, mana: 0, turns: 0 },
  drain: { name: 'drain', cost: 73, attack: 2, armor: 0, heal: 2, mana: 0, turns: 0 },
  shield: { name: 'shield', cost: 113, attack: 0, armor: 7, heal: 0, mana: 0, turns: 6 },
  poison: { name: 'poison', cost: 173, attack: 3, armor: 0, heal: 0, mana: 0, turns: 6 },
  recharge: { name: 'recharge', cost: 229, attack: 0, armor: 0, heal: 0, mana: 101, turns: 5 },
};

let minimumMana = 10 ** 15;

class Wizard {
  constructor(hp, mana) {
    this.hp = hp;
    this.mana = mana;
    this.attack = 1;
    this.armor = 0;
    this.effects = [];
    this.manaUsed = 0;
  }

  fastCopy() {
    const newWizard = new Wizard(this.hp, this.mana);
    newWizard.attack = this.attack;
    newWizard.armor = this.armor;
    newWizard.effects = this.effects.map((eff) => ({ ...eff }));
    newWizard.manaUsed = this.manaUsed;
    return newWizard;
  }
}

function applyEffects(player, boss) {
  player.armor = 0;

  const ending = [];
  for (let idx = 0; idx < player.effects.length; idx++) {
    const spell = player.effects[idx];
    boss.hp -= spell.attack;
    player.mana += spell.mana;
    player.armor += spell.armor;
    player.effects[idx].turns -= 1;

    if (player.effects[idx].turns === 0) {
      ending.push(idx);
    }
  }

  ending.sort((a, b) => b - a);
  for (const i of ending) {
    player.effects.splice(i, 1);
  }

  return boss.hp < 0;
}

function processBossAttack(player, boss, currentMinimum) {
  player.hp -= Math.max(1, boss.attack - player.armor);

  if (player.hp <= 0) {
    return currentMinimum;
  }

  return null;
}

function tryNextSpells(player, boss, currentMinimum) {
  const invalidSpells = player.effects.map((spell) => spell.name);
  const costs = [currentMinimum];

  for (const spell of Object.values(spells)) {
    if (invalidSpells.includes(spell.name)) {
      continue;
    }
    if (spell.cost <= player.mana) {
      const result = resolveTurn(player.fastCopy(), boss.fastCopy(), spell);
      if (typeof result === 'number') {
        costs.push(result);
      }
    }
  }

  minimumMana = Math.min(...costs);
  return minimumMana;
}

function resolveTurn(player, boss, spell) {
  if (player.manaUsed > minimumMana) {
    return player.manaUsed;
  }

  player.mana -= spell.cost;
  player.manaUsed += spell.cost;

  if (spell.turns > 0) {
    player.effects.push({ ...spell });
  } else {
    boss.hp -= spell.attack;
    player.hp += spell.heal;
  }

  if (boss.hp < 0) {
    return player.manaUsed;
  }

  if (applyEffects(player, boss)) {
    return player.manaUsed;
  }

  const result = processBossAttack(player, boss, minimumMana);
  if (result !== null) {
    return result;
  }

  // HARD MODE: Player loses 1 HP at the start of each player turn
  player.hp -= 1;
  if (player.hp <= 0) {
    return minimumMana;
  }

  if (applyEffects(player, boss)) {
    return player.manaUsed;
  }

  return tryNextSpells(player, boss, minimumMana);
}

function solvePart2() {
  const player = new Wizard(50, 500);
  const boss = new Wizard(55, 0);
  boss.attack = 8;

  // HARD MODE: Player loses 1 HP at the start of the first turn
  player.hp -= 1;

  for (const spell of Object.values(spells)) {
    const result = resolveTurn(player.fastCopy(), boss.fastCopy(), spell);
    if (typeof result === 'number') {
      minimumMana = Math.min(minimumMana, result);
    }
  }

  return minimumMana;
}

const answer = solvePart2();
console.log(`Part 2: ${answer}`);
