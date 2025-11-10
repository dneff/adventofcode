"""
Advent of Code 2019 - Day 8: Space Image Format - Part 2

Decode the actual image by compositing the layers. Each pixel can be:
- 0 (black)
- 1 (white)
- 2 (transparent)
The final image is formed by stacking layers and using the first non-transparent
pixel for each position.
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


def composite_layers(layers):
    """
    Composite image layers to form final image.

    For each pixel position, use the first non-transparent (non-2) value
    encountered when iterating through layers front to back.

    Args:
        layers: List of layer strings

    Returns:
        Final composited image string
    """
    composited_pixels = []

    # For each pixel position in a layer
    for pixel_index in range(len(layers[0])):
        # Check layers from front to back
        for layer in layers:
            pixel_value = layer[pixel_index]
            if pixel_value != '2':  # Not transparent
                # Convert to display character
                if pixel_value == '0':
                    composited_pixels.append(' ')  # Black = space
                else:
                    composited_pixels.append('*')  # White = asterisk
                break

    return ''.join(composited_pixels)


def format_image_for_display(image_string):
    """
    Format the linear image string as rows for display.

    Args:
        image_string: Composited image as single string

    Returns:
        Multi-line string with image formatted in rows
    """
    lines = ["The image is:"]

    for row in range(IMAGE_HEIGHT):
        start = row * IMAGE_WIDTH
        end = start + IMAGE_WIDTH
        lines.append(image_string[start:end])

    return '\n'.join(lines)


def solve_part2():
    """Decode and display the final composited image."""
    image_data = AoCInput.read_file(INPUT_FILE).strip()
    layers = parse_image_layers(image_data)

    # Composite layers to get final image
    final_image = composite_layers(layers)

    # Format for display
    return format_image_for_display(final_image)


answer = solve_part2()
print(answer)
