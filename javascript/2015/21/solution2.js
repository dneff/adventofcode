/**
 * Advent of Code 2015 - Day 21: RPG Simulator 20XX
 * https://adventofcode.com/2015/day/21
 *
 * Find the most expensive equipment loadout that loses against the boss.
 */

import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const INPUT_FILE = join(__dirname, '../../../aoc-data/2015/21/input');

const itemShop = {
  weapons: {
    dagger: { cost: 8, attack: 4, armor: 0 },
    shortsword: { cost: 10, attack: 5, armor: 0 },
    warhammer: { cost: 25, attack: 6, armor: 0 },
    longsword: { cost: 40, attack: 7, armor: 0 },
    greataxe: { cost: 74, attack: 8, armor: 0 },
  },
  armors: {
    none: { cost: 0, attack: 0, armor: 0 },
    leather: { cost: 13, attack: 0, armor: 1 },
    chainmail: { cost: 31, attack: 0, armor: 2 },
    splintmail: { cost: 53, attack: 0, armor: 3 },
    bandedmail: { cost: 75, attack: 0, armor: 4 },
    platemail: { cost: 102, attack: 0, armor: 5 },
  },
  rings: {
    none: { cost: 0, attack: 0, armor: 0 },
    dmg_1: { cost: 25, attack: 1, armor: 0 },
    dmg_2: { cost: 50, attack: 2, armor: 0 },
    dmg_3: { cost: 100, attack: 3, armor: 0 },
    def_1: { cost: 20, attack: 0, armor: 1 },
    def_2: { cost: 40, attack: 0, armor: 2 },
    def_3: { cost: 80, attack: 0, armor: 3 },
  },
};

class Fighter {
  constructor() {
    this.hp = 0;
    this.attack = 1;
    this.armor = 0;
    this.cost = 0;
  }

  fight(monster) {
    let myHp = this.hp;
    let theirHp = monster.hp;
    while (myHp > 0) {
      theirHp -= Math.max(1, this.attack - monster.armor);
      if (theirHp <= 0) {
        return true;
      }
      myHp -= Math.max(1, monster.attack - this.armor);
    }
    return false;
  }

  equip(cost, attack, armor) {
    this.cost = cost;
    this.attack = attack;
    this.armor = armor;
  }
}

function* getMostExpensiveOutfit() {
  const outfits = {};
  for (const weapon of Object.keys(itemShop.weapons)) {
    for (const armor of Object.keys(itemShop.armors)) {
      for (const r1 of Object.keys(itemShop.rings)) {
        for (const r2 of Object.keys(itemShop.rings)) {
          if (r1 === r2 && r1 !== 'none') {
            continue;
          }
          const outfitCost =
            itemShop.weapons[weapon].cost +
            itemShop.armors[armor].cost +
            itemShop.rings[r1].cost +
            itemShop.rings[r2].cost;

          const outfitAttack =
            itemShop.weapons[weapon].attack +
            itemShop.armors[armor].attack +
            itemShop.rings[r1].attack +
            itemShop.rings[r2].attack;

          const outfitArmor =
            itemShop.weapons[weapon].armor +
            itemShop.armors[armor].armor +
            itemShop.rings[r1].armor +
            itemShop.rings[r2].armor;

          if (!outfits[outfitCost]) {
            outfits[outfitCost] = [];
          }
          outfits[outfitCost].push([outfitAttack, outfitArmor]);
        }
      }
    }
  }

  const prices = Object.keys(outfits)
    .map(Number)
    .sort((a, b) => b - a);

  for (const p of prices) {
    for (const outfit of outfits[p]) {
      yield [p, outfit[0], outfit[1]];
    }
  }
}

function solvePart2() {
  const player = new Fighter();
  player.hp = 100;

  const boss = new Fighter();
  boss.hp = 104;
  boss.attack = 8;
  boss.armor = 1;

  const outfits = getMostExpensiveOutfit();

  let outfit = outfits.next().value;
  player.equip(...outfit);
  while (player.fight(boss)) {
    outfit = outfits.next().value;
    player.equip(...outfit);
  }
  return player.cost;
}

const answer = solvePart2();
console.log(`Part 2: ${answer}`);
