"""
Advent of Code 2019 - Day 8: Space Image Format - Part 1

Decode a corrupted image from the Digital Sending Network. The image is transmitted
as layers of pixels (25 wide x 6 tall). Find the layer with the fewest 0 digits,
then calculate the number of 1 digits multiplied by the number of 2 digits on that layer.
"""
import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2019/8/input')

# Image dimensions
IMAGE_WIDTH = 25
IMAGE_HEIGHT = 6
LAYER_SIZE = IMAGE_WIDTH * IMAGE_HEIGHT


def parse_image_layers(image_data):
    """
    Split image data into layers of pixels.

    Args:
        image_data: String of digits representing the image

    Returns:
        List of layer strings, each containing LAYER_SIZE digits
    """
    layers = []
    for i in range(0, len(image_data), LAYER_SIZE):
        layers.append(image_data[i:i + LAYER_SIZE])
    return layers


def solve_part1():
    """Find checksum: (1 digits * 2 digits) on layer with fewest 0 digits."""
    image_data = AoCInput.read_file(INPUT_FILE).strip()
    layers = parse_image_layers(image_data)

    # Map: number of zeros -> checksum value for that layer
    layer_checksums = {}

    for layer in layers:
        zero_count = layer.count('0')
        checksum = layer.count('1') * layer.count('2')
        layer_checksums[zero_count] = checksum

    # Return checksum for layer with minimum zero count
    min_zeros = min(layer_checksums.keys())
    return layer_checksums[min_zeros]


answer = solve_part1()
AoCUtils.print_solution(1, answer)