"""
Advent of Code 2019 - Day 23: Category Six - Part 1

Simulate a network of 50 IntCode computers communicating via packets.
Find the Y value of the first packet sent to address 255.

Network Protocol:
- Each computer has a network address (0-49)
- Computers communicate by sending packets with (destination, X, Y) values
- When a computer has no input, it receives -1
- Address 255 is a special destination we're monitoring for the answer
"""
import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402
from IntCode import IntCode, InputInterrupt, OutputInterrupt  # noqa: E402
from collections import deque  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2019/23/input')

# Read the IntCode program that will run on each computer
intcode_program = AoCInput.read_file(INPUT_FILE).strip()

# Create a network of 50 computers, each running the same IntCode program
computers = [IntCode(intcode_program) for _ in range(50)]

# Each computer has its own packet queue for incoming messages
packet_queues = [deque() for _ in range(50)]

answer = None

# Initialize each computer with its network address (0-49)
# The first input each computer receives is its own network address
for network_address, computer in enumerate(computers):
    computer.push(network_address)

# Main network simulation loop
# We'll run all computers in a round-robin fashion until we find a packet sent to address 255
try:
    while True:
        # Process each computer in the network in sequence (round-robin scheduling)
        for network_address, computer in enumerate(computers):
            # Provide input to the computer: either a pending packet or -1 (idle signal)
            if packet_queues[network_address]:
                # Computer has a packet waiting in its queue - deliver the X and Y values
                x, y = packet_queues[network_address].popleft()
                computer.push(x)
                computer.push(y)
            else:
                # Computer has no packets - send -1 to signal that its input queue is empty
                computer.push(-1)

            # Run the computer until it needs more input
            # The computer will run until it either requests input or produces complete packets
            should_continue_running = True
            while should_continue_running:
                try:
                    computer.run()
                    # If we have a partial packet (not divisible by 3), keep running to get complete packets
                    should_continue_running = len(computer.output) % 3 != 0
                except InputInterrupt:
                    # Computer needs more input - stop running and move to next computer
                    should_continue_running = False
                except OutputInterrupt:
                    # Computer has produced some output - check if we have complete packets
                    # A complete packet is 3 values: (destination, X, Y)
                    if len(computer.output) % 3 != 0:
                        # Partial packet - keep running to get the rest
                        continue

                    # Process all complete packets this computer has produced
                    while computer.output:
                        # Pop values in reverse order (destination was output first, so it's last in the output list)
                        destination = computer.pop()
                        x = computer.pop()
                        y = computer.pop()

                        # Validate destination address is in valid range (0-255)
                        if destination < 0 or destination > 255:
                            raise ValueError(f"Invalid destination address: {destination}")

                        print(f"Computer {network_address} sent packet ({x}, {y}) to address {destination}")

                        # Check if this packet is sent to address 255 (the special monitoring address)
                        if destination == 255:
                            answer = y
                            # Use StopIteration to cleanly break out of all nested loops
                            raise StopIteration

                        # Queue the packet for delivery to the destination computer
                        packet_queues[destination].append((x, y))
except StopIteration:
    # Successfully found the answer - first packet sent to address 255
    pass

AoCUtils.print_solution(1, answer)
