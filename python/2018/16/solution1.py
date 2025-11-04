"""
Advent of Code 2018 - Day 16: Chronal Classification
https://adventofcode.com/2018/day/16

Reverse-engineer a device with four registers and 16 opcodes. Given sample instruction
executions showing before/after register states, determine how many samples behave like
three or more opcodes.

Part 1: Count samples that behave like three or more opcodes.
"""

import os
import sys
import ast

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2018/16/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


class WristDevice:
    """Simulates a wrist device with 4 registers and 16 opcodes."""

    def __init__(self):
        self.registers = [0, 0, 0, 0]

    def set_registers(self, values):
        """Set register values from a list."""
        self.registers = list(values)

    def get_registers(self):
        """Get current register values."""
        return list(self.registers)

    # Addition operations
    def addr(self, a, b, c):
        """Add register: registers[c] = registers[a] + registers[b]"""
        self.registers[c] = self.registers[a] + self.registers[b]

    def addi(self, a, b, c):
        """Add immediate: registers[c] = registers[a] + b"""
        self.registers[c] = self.registers[a] + b

    # Multiplication operations
    def mulr(self, a, b, c):
        """Multiply register: registers[c] = registers[a] * registers[b]"""
        self.registers[c] = self.registers[a] * self.registers[b]

    def muli(self, a, b, c):
        """Multiply immediate: registers[c] = registers[a] * b"""
        self.registers[c] = self.registers[a] * b

    # Bitwise AND operations
    def banr(self, a, b, c):
        """Bitwise AND register: registers[c] = registers[a] & registers[b]"""
        self.registers[c] = self.registers[a] & self.registers[b]

    def bani(self, a, b, c):
        """Bitwise AND immediate: registers[c] = registers[a] & b"""
        self.registers[c] = self.registers[a] & b

    # Bitwise OR operations
    def borr(self, a, b, c):
        """Bitwise OR register: registers[c] = registers[a] | registers[b]"""
        self.registers[c] = self.registers[a] | self.registers[b]

    def bori(self, a, b, c):
        """Bitwise OR immediate: registers[c] = registers[a] | b"""
        self.registers[c] = self.registers[a] | b

    # Assignment operations
    def setr(self, a, b, c):
        """Set register: registers[c] = registers[a]"""
        self.registers[c] = self.registers[a]

    def seti(self, a, b, c):
        """Set immediate: registers[c] = a"""
        self.registers[c] = a

    # Greater-than testing
    def gtir(self, a, b, c):
        """Greater-than immediate/register: registers[c] = 1 if a > registers[b] else 0"""
        self.registers[c] = 1 if a > self.registers[b] else 0

    def gtri(self, a, b, c):
        """Greater-than register/immediate: registers[c] = 1 if registers[a] > b else 0"""
        self.registers[c] = 1 if self.registers[a] > b else 0

    def gtrr(self, a, b, c):
        """Greater-than register/register: registers[c] = 1 if registers[a] > registers[b] else 0"""
        self.registers[c] = 1 if self.registers[a] > self.registers[b] else 0

    # Equality testing
    def eqir(self, a, b, c):
        """Equal immediate/register: registers[c] = 1 if a == registers[b] else 0"""
        self.registers[c] = 1 if a == self.registers[b] else 0

    def eqri(self, a, b, c):
        """Equal register/immediate: registers[c] = 1 if registers[a] == b else 0"""
        self.registers[c] = 1 if self.registers[a] == b else 0

    def eqrr(self, a, b, c):
        """Equal register/register: registers[c] = 1 if registers[a] == registers[b] else 0"""
        self.registers[c] = 1 if self.registers[a] == self.registers[b] else 0

    def get_all_opcodes(self):
        """Return list of all opcode methods."""
        return [
            self.addr, self.addi, self.mulr, self.muli,
            self.banr, self.bani, self.borr, self.bori,
            self.setr, self.seti,
            self.gtir, self.gtri, self.gtrr,
            self.eqir, self.eqri, self.eqrr
        ]


def parse_samples(lines):
    """
    Parse instruction samples from input.

    Each sample consists of:
    - Before: [r0, r1, r2, r3]
    - Instruction: [opcode, a, b, c]
    - After: [r0, r1, r2, r3]

    Returns:
        list: List of sample dictionaries
    """
    samples = []
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # Stop at blank lines (indicates end of samples section)
        if not line:
            i += 1
            # Check for multiple consecutive blank lines (end of samples)
            if i < len(lines) and not lines[i].strip():
                break
            continue

        # Parse a sample
        if line.startswith('Before:'):
            before = ast.literal_eval(line.split(': ')[1])
            instruction = [int(x) for x in lines[i + 1].split()]
            after = ast.literal_eval(lines[i + 2].split(':  ')[1])

            samples.append({
                'before': before,
                'instruction': instruction,
                'after': after
            })

            i += 3
        else:
            i += 1

    return samples


def count_matching_opcodes(device, sample):
    """
    Count how many opcodes produce the expected output for a sample.

    Args:
        device: WristDevice instance
        sample: Dictionary with 'before', 'instruction', 'after'

    Returns:
        int: Number of opcodes that match
    """
    instruction = sample['instruction']
    a, b, c = instruction[1], instruction[2], instruction[3]

    matches = 0
    for opcode_func in device.get_all_opcodes():
        device.set_registers(sample['before'])
        opcode_func(a, b, c)
        if device.get_registers() == sample['after']:
            matches += 1

    return matches


def solve_part1():
    """
    Count how many samples behave like three or more opcodes.

    Returns:
        int: Number of samples matching 3+ opcodes
    """
    lines = AoCInput.read_lines(INPUT_FILE)
    samples = parse_samples(lines)

    device = WristDevice()
    count = 0

    for sample in samples:
        if count_matching_opcodes(device, sample) >= 3:
            count += 1

    return count


# Compute and print the answer
answer = solve_part1()
AoCUtils.print_solution(1, answer)
