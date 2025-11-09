/**
 * Advent of Code 2015 - Day 7, Part 2
 * https://adventofcode.com/2015/day/7
 *
 * Simulates the circuit twice, overriding wire 'b' with the result from wire 'a'.
 */

import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const INPUT_FILE = join(__dirname, '../../../aoc-data/2015/7/input');

class Circuit {
  constructor() {
    this.wireSignals = {};
  }

  hasSignal(...wireOrValues) {
    for (const inputValue of wireOrValues) {
      if (
        typeof inputValue !== 'number' &&
        !/^\d+$/.test(inputValue) &&
        !(inputValue in this.wireSignals)
      ) {
        return false;
      }
    }
    return true;
  }

  getValue(input) {
    if (typeof input === 'number' || /^\d+$/.test(input)) {
      return parseInt(input, 10);
    }
    return this.wireSignals[input];
  }

  AND(leftInput, rightInput) {
    if (!this.hasSignal(leftInput, rightInput)) {
      throw new Error('no signal for wire');
    }
    return this.getValue(leftInput) & this.getValue(rightInput);
  }

  OR(leftInput, rightInput) {
    if (!this.hasSignal(leftInput, rightInput)) {
      throw new Error('no signal for wire');
    }
    return this.getValue(leftInput) | this.getValue(rightInput);
  }

  LSHIFT(wireInput, shiftAmount) {
    if (!this.hasSignal(wireInput, shiftAmount)) {
      throw new Error('no signal for wire');
    }
    return this.getValue(wireInput) << this.getValue(shiftAmount);
  }

  RSHIFT(wireInput, shiftAmount) {
    if (!this.hasSignal(wireInput, shiftAmount)) {
      throw new Error('no signal for wire');
    }
    return this.getValue(wireInput) >>> this.getValue(shiftAmount);
  }

  NOT(wireInput) {
    if (!this.hasSignal(wireInput)) {
      throw new Error('no signal for wire');
    }
    return (~this.getValue(wireInput)) & 0xffff;
  }

  processDirectAssignment(sourcePart, destWire) {
    if (!this.hasSignal(sourcePart)) {
      return false;
    }
    this.wireSignals[destWire] = this.getValue(sourcePart);
    return true;
  }

  processNotOperation(sourceWire, destWire) {
    if (!this.hasSignal(sourceWire)) {
      return false;
    }
    this.wireSignals[destWire] = this.NOT(sourceWire);
    return true;
  }

  processBinaryOperation(leftInput, operation, rightInput, destWire) {
    if (!this.hasSignal(leftInput, rightInput)) {
      return false;
    }
    this.wireSignals[destWire] = this[operation](leftInput, rightInput);
    return true;
  }

  processInstruction(instruction) {
    const [sourceExpr, destWire] = instruction.split(' -> ');
    const sourceParts = sourceExpr.split(' ');

    try {
      if (sourceParts.length === 1) {
        return this.processDirectAssignment(sourceParts[0], destWire);
      } else if (sourceParts.length === 2) {
        return this.processNotOperation(sourceParts[1], destWire);
      } else {
        const [leftInput, gateOperation, rightInput] = sourceParts;
        return this.processBinaryOperation(leftInput, gateOperation, rightInput, destWire);
      }
    } catch (error) {
      return false;
    }
  }
}

function solvePart2() {
  const lines = readFileSync(INPUT_FILE, 'utf-8').trim().split('\n');

  // First run: Get the signal on wire 'a'
  let circuit = new Circuit();
  let pendingInstructions = lines.map((line) => line.trim());

  while (pendingInstructions.length > 0) {
    const deferredInstructions = [];
    for (const instruction of pendingInstructions) {
      if (!circuit.processInstruction(instruction)) {
        deferredInstructions.push(instruction);
      }
    }
    pendingInstructions = deferredInstructions;
  }

  const signalFromA = circuit.wireSignals['a'];

  // Second run: Reset circuit and override wire 'b'
  circuit = new Circuit();
  circuit.wireSignals['b'] = signalFromA;

  // Re-process instructions, but skip any that assign to wire 'b'
  pendingInstructions = lines
    .map((line) => line.trim())
    .filter((inst) => !inst.endsWith(' -> b'));

  while (pendingInstructions.length > 0) {
    const deferredInstructions = [];
    for (const instruction of pendingInstructions) {
      if (!circuit.processInstruction(instruction)) {
        deferredInstructions.push(instruction);
      }
    }
    pendingInstructions = deferredInstructions;
  }

  return circuit.wireSignals['a'];
}

const answer = solvePart2();
console.log(`Part 2: ${answer}`);
