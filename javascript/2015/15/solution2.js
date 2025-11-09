/**
 * Advent of Code 2015 - Day 15: Science for Hungry People
 * https://adventofcode.com/2015/day/15
 *
 * Finds the highest-scoring cookie recipe with exactly 500 calories.
 */

import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const INPUT_FILE = join(__dirname, '../../../aoc-data/2015/15/input');

class Ingredient {
  constructor(name, capacity, durability, flavor, texture, calories) {
    this.name = name;
    this.capacity = capacity;
    this.durability = durability;
    this.flavor = flavor;
    this.texture = texture;
    this.calories = calories;
  }
}

function scoreRecipe(ingredients, measures, calorieTarget) {
  const properties = ['capacity', 'durability', 'flavor', 'texture'];
  const propertyScores = {};

  const totalCalories = ingredients.reduce((sum, ing, i) => sum + ing.calories * measures[i], 0);
  if (totalCalories !== calorieTarget) {
    return 0;
  }

  for (const prop of properties) {
    propertyScores[prop] = 0;
    for (let i = 0; i < ingredients.length; i++) {
      propertyScores[prop] += measures[i] * ingredients[i][prop];
    }
  }

  const valid = Object.values(propertyScores).filter(x => x > 0);
  const result = valid.reduce((a, b) => a * b, 1);
  return result;
}

function solvePart2() {
  const lines = readFileSync(INPUT_FILE, 'utf-8').trim().split('\n');

  const ingredients = [];
  const maxCount = 100;
  const calorieTarget = 500;

  for (const line of lines) {
    const cleaned = line.replace(/,/g, '').replace(/:/g, '');
    const parts = cleaned.split(' ');
    const name = parts[0];
    const numbers = parts.filter(x => /^-?\d+$/.test(x)).map(Number);
    const [capacity, durability, flavor, texture, calories] = numbers;
    ingredients.push(new Ingredient(name, capacity, durability, flavor, texture, calories));
  }

  let maxScore = 0;
  for (let i1 = 1; i1 < maxCount; i1++) {
    for (let i2 = 1; i2 < maxCount - i1; i2++) {
      for (let i3 = 1; i3 < maxCount - i1 - i2; i3++) {
        const i4 = maxCount - i1 - i2 - i3;
        const weights = [i1, i2, i3, i4];
        maxScore = Math.max(maxScore, scoreRecipe(ingredients, weights, calorieTarget));
      }
    }
  }

  return maxScore;
}

const answer = solvePart2();
console.log(`Part 2: ${answer}`);
