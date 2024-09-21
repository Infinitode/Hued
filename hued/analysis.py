"""
Module: analysis.py

This module provides functions to analyze the properties of colors.
It includes methods to determine the temperature, neutrality, brightness,
and whether a color is pastel, muted, or vibrant.

Functions:
    - get_temperature: Determines the temperature of a color based on its RGB values.
    - is_neutral: Checks if a color is neutral.
    - brightness: Calculates the brightness of a color.
    - is_pastel: Checks if a color is pastel.
    - is_muted: Checks if a color is muted.
    - is_vibrant: Checks if a color is vibrant.
"""

from hued.conversions import rgb_to_hsv

def get_temperature(rgb):
    """
    Determine the temperature of a color based on its RGB values.

    Parameters:
    rgb (tuple): A tuple containing the RGB values (r, g, b).

    Returns:
    str: "Warm" if the color is warm, "Cool" if cool, or "Neutral" if neither.
    """
    r, g, b = rgb
    if r > g and r > b:
        return "Warm"
    elif b > r and b > g:
        return "Cool"
    else:
        return "Neutral"

def is_neutral(rgb):
    """
    Check if a color is neutral.

    Parameters:
    rgb (tuple): A tuple containing the RGB values (r, g, b).

    Returns:
    bool: True if the color is neutral, False otherwise.
    """
    r, g, b = rgb
    return abs(r - g) < 30 and abs(g - b) < 30 and abs(r - b) < 30

def brightness(rgb):
    """
    Calculate the brightness of a color.

    Parameters:
    rgb (tuple): A tuple containing the RGB values (r, g, b).

    Returns:
    float: The brightness of the color as a value between 0 and 1.
    """
    r, g, b = rgb
    return (0.299 * r + 0.587 * g + 0.114 * b) / 255

def is_pastel(rgb):
    """
    Check if a color is pastel.

    Parameters:
    rgb (tuple): A tuple containing the RGB values (r, g, b).

    Returns:
    bool: True if the color is pastel, False otherwise.
    """
    r, g, b = rgb
    return all(value > 127 for value in rgb) and brightness(rgb) > 0.5

def is_muted(rgb):
    """
    Check if a color is muted.

    Parameters:
    rgb (tuple): A tuple containing the RGB values (r, g, b).

    Returns:
    bool: True if the color is muted, False otherwise.
    """
    r, g, b = rgb
    # Calculate brightness
    brightness = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    # Calculate saturation (simple approach)
    max_rgb = max(r, g, b)
    min_rgb = min(r, g, b)
    saturation = (max_rgb - min_rgb) / max_rgb if max_rgb > 0 else 0

    return brightness < 0.5 and saturation < 0.5  # Adjust thresholds as needed

def is_vibrant(rgb):
    """
    Check if a color is vibrant.

    Parameters:
    rgb (tuple): A tuple containing the RGB values (r, g, b).

    Returns:
    bool: True if the color is vibrant, False otherwise.
    """
    r, g, b = rgb

    _, s, v = rgb_to_hsv(r, g, b)
    # Define thresholds for vibrancy
    saturation_threshold = 0.5
    value_threshold = 0.7

    # Check if the color is vibrant
    return s > saturation_threshold and v > value_threshold