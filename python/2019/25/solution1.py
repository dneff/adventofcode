"""
Advent of Code 2019 - Day 25: Cryostatis
https://adventofcode.com/2019/day/25

This droid can follow basic instructions and report on its surroundings; 
you can communicate with it through an Intcode program (your puzzle input) 
running on an ASCII-capable computer.

As the droid moves through its environment, it will describe what it 
encounters. When it says Command?, you can give it a single instruction 
terminated with a newline (ASCII code 10).

Possible instructions are:
Movement via north, south, east, or west.

To take an item the droid sees in the environment, use the command 
take <name of item>. For example, if the droid reports seeing a red ball, 
you can pick it up with take red ball.

To drop an item the droid is carrying, use the command drop <name of item>. 
For example, if the droid is carrying a green ball, you can drop it with 
drop green ball.

To get a list of all of the items the droid is currently carrying, use the 
command inv (for "inventory").

Extra spaces or other characters aren't allowed - instructions must be provided precisely.

Santa's ship is a Reindeer-class starship; these ships use pressure-sensitive 
floors to determine the identity of droids and crew members. The standard 
configuration for these starships is for all droids to weigh exactly the same 
amount to make them easier to detect. If you need to get past such a sensor, 
you might be able to reach the correct weight by carrying items from the 
environment.

Look around the ship and see if you can find the password for the main airlock.

Strategy:
This is a text adventure game where you have to explore the ship and find the 
password for the main airlock. The ship has multiple rooms, and you can move
between them using the north, south, east, and west commands. You can also take
items from the environment and use them to navigate through the ship. The goal is
to find the correct combination of items to carry so that you can pass through the
pressure-sensitive floor and reach the main airlock.

The solution involves exploring the ship, taking items, and using them to navigate
through the ship and find the password for the main airlock.

A couple of hints for solving this puzzle:
- Assume the items in the inventory are listed in order of their weight, from lightest to heaviest.
- Try carrying different combinations of items and see if any of them allow
    you to pass through the pressure-sensitive floor.
- The total number of items required to pass through the pressure-sensitive floor is 4.

"""

import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "../../"))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402
from IntCode import IntCode, OutputInterrupt, InputInterrupt  # noqa: E402


# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, "../../../../aoc-data/2019/25/input")

program = AoCInput.read_file(INPUT_FILE)
droid = IntCode(program)
droid.complete = False

# Collect camera view
camera_output = []
while not droid.complete:
    try:
        droid.run()
    except OutputInterrupt:
        ascii_value = chr(int(droid.pop()))
        camera_output.append(ascii_value)
    except InputInterrupt:
        output = ''.join(camera_output).strip()
        camera_output = []
        instruction = input(f"{output}:")
        for char in instruction:
            droid.push(ord(char))
        droid.push(10)

print(''.join(camera_output).strip())
