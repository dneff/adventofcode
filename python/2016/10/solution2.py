"""
Advent of Code 2016 - Day 10: Balance Bots (Part 2)

Problem: A factory has bots that exchange microchips. Each bot holds two chips
and distributes them according to instructions - giving the lower-value chip
to one destination and the higher-value chip to another destination.
Destinations can be other bots or output bins.

Goal: After all bots have finished processing, multiply together the values of
one chip in each of outputs 0, 1, and 2.
"""

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2016/10/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils
from collections import defaultdict

def main():
    # Store instructions for each bot: [(low_dest_type, low_dest_id), (high_dest_type, high_dest_id)]
    bot_instructions = defaultdict(list)

    # Track chips held by each bot (identified by bot number string)
    bot_chips = defaultdict(list)

    # Track chips in output bins
    output_bins = defaultdict(list)

    # Initial chip assignments (before processing)
    initial_values = []

    def process_bot(bot_id):
        """
        Process a bot that has two chips: distribute them according to instructions.
        The lower-value chip goes to the first destination, higher-value to the second.
        """
        chips = bot_chips[bot_id][:]
        chips.sort()  # Sort to get [lower_value, higher_value]

        # Clear the bot's chips and distribute them
        bot_chips[bot_id].clear()

        # Process low chip (index 0) and high chip (index 1)
        for chip_index, (dest_type, dest_id) in enumerate(bot_instructions[bot_id]):
            chip_value = chips[chip_index]

            if dest_type == 'output':
                output_bins[dest_id].append(chip_value)
            else:  # dest_type == 'bot'
                bot_chips[dest_id].append(chip_value)
                # If the destination bot now has 2 chips, process it
                if len(bot_chips[dest_id]) == 2:
                    process_bot(dest_id)

    # Parse input instructions
    lines = AoCInput.read_lines(INPUT_FILE)
    for line in lines:
        words = line.strip().split()

        if words[0] == "bot":
            # Format: "bot X gives low to [bot|output] Y and high to [bot|output] Z"
            bot_id = words[1]
            low_dest_type = words[5]   # 'bot' or 'output'
            low_dest_id = words[6]
            high_dest_type = words[10]  # 'bot' or 'output'
            high_dest_id = words[11]
            bot_instructions[bot_id] = [(low_dest_type, low_dest_id), (high_dest_type, high_dest_id)]
        else:
            # Format: "value X goes to bot Y"
            chip_value = int(words[1])
            bot_id = words[5]
            initial_values.append((bot_id, chip_value))

    # Give initial chips to bots and start processing
    for bot_id, chip_value in initial_values:
        bot_chips[bot_id].append(chip_value)
        # If this bot now has 2 chips, process it
        if len(bot_chips[bot_id]) == 2:
            process_bot(bot_id)

    # Calculate the product of chips in outputs 0, 1, and 2
    result = output_bins['0'][0] * output_bins['1'][0] * output_bins['2'][0]
    AoCUtils.print_solution(2, result)

if __name__ == "__main__":
    main()