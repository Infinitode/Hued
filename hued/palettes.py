"""
Module: palettes.py

This module provides functionality for generating various color palettes based on a given base color.
It includes methods to create complementary, analogous, triadic, monochromatic, and random palettes.

Classes:
    - ColorPalette: Represents a color palette based on a specified base color.

Methods:
    - ColorPalette.__init__: Initializes the color palette with a base color.
    - ColorPalette.generate_complementary: Generates a complementary color palette.
    - ColorPalette.generate_analogous: Generates an analogous color palette.
    - ColorPalette.generate_triadic: Generates a triadic color palette.
    - ColorPalette.generate_monochromatic: Generates a monochromatic color palette.
    - ColorPalette.palette_to_hex: Converts the palette colors to their HEX representations.
    - ColorPalette.generate_random_palette: Generates a random color and its corresponding palettes.
"""

import random
from hued.conversions import rgb_to_hsl, hsl_to_rgb, rgb_to_hex

class ColorPalette:
    """
    A class to create and manipulate color palettes.
    
    Attributes:
        base_color (tuple): The RGB tuple of the base color.
        palette (list): A list of RGB tuples representing the color palette.
    """
    
    def __init__(self, base_color):
        """
        Initializes the ColorPalette with a base color.

        Parameters:
            base_color (tuple): The RGB tuple of the base color (0-255).
        """
        self.base_color = base_color
        self.palette = [base_color]

    def generate_complementary(self):
        """
        Generates a complementary color palette.

        Returns:
            list: A list of RGB tuples representing the complementary palette.
        """
        h, s, l = rgb_to_hsl(*self.base_color)
        complementary_h = (h + 180) % 360
        complementary_color = hsl_to_rgb(complementary_h, s, l)
        self.palette = [self.base_color, complementary_color]
        return self.palette

    def generate_analogous(self, angle=30):
        """
        Generates an analogous color palette.

        Parameters:
            angle (int): The angle difference for analogous colors (default 30).

        Returns:
            list: A list of RGB tuples representing the analogous palette.
        """
        h, s, l = rgb_to_hsl(*self.base_color)
        analogous1_h = (h + angle) % 360
        analogous2_h = (h - angle) % 360
        analogous1 = hsl_to_rgb(analogous1_h, s, l)
        analogous2 = hsl_to_rgb(analogous2_h, s, l)
        self.palette = [analogous2, self.base_color, analogous1]
        return self.palette

    def generate_triadic(self):
        """
        Generates a triadic color palette.

        Returns:
            list: A list of RGB tuples representing the triadic palette.
        """
        h, s, l = rgb_to_hsl(*self.base_color)
        triadic1_h = (h + 120) % 360
        triadic2_h = (h - 120) % 360
        triadic1 = hsl_to_rgb(triadic1_h, s, l)
        triadic2 = hsl_to_rgb(triadic2_h, s, l)
        self.palette = [self.base_color, triadic1, triadic2]
        return self.palette

    def generate_monochromatic(self, shades=24):
        """
        Generates a monochromatic color palette with varying lightness.

        Parameters:
            shades (int): Number of shades to generate (default 5).

        Returns:
            list: A list of RGB tuples representing the monochromatic palette.
        """
        h, s, l = rgb_to_hsl(*self.base_color)

        # Generate unique lightness values
        lightness_values = []
        for i in range(shades):
            new_lightness = max(min(l + (i / (shades - 1)) - 0.5, 1), 0)
            if new_lightness not in lightness_values:  # Avoid duplicates
                lightness_values.append(new_lightness)

        self.palette = [hsl_to_rgb(h, s, lightness) for lightness in lightness_values]
        return self.palette

    def palette_to_hex(self):
        """
        Converts the RGB palette to HEX format.

        Returns:
            list: A list of HEX strings representing the palette.
        """
        return [rgb_to_hex(*color).upper() for color in self.palette]

    def add_color(self, rgb_color):
        """
        Adds a color to the palette.

        Parameters:
            rgb_color (tuple): An RGB tuple (0-255).
        """
        self.palette.append(rgb_color)

    def remove_color(self, rgb_color):
        """
        Removes a color from the palette if it exists.

        Parameters:
            rgb_color (tuple): An RGB tuple (0-255).
        """
        if rgb_color in self.palette:
            self.palette.remove(rgb_color)

    def generate_random_palette(self):
        """Generates a random base color and its associated palettes."""
        # Generate a random RGB color
        base_color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )

        self.base_color = base_color
        print(f"Random Base Color: {base_color}")

        # Generate the palettes
        complementary = self.generate_complementary()
        analogous = self.generate_analogous()
        triadic = self.generate_triadic()
        monochromatic = self.generate_monochromatic()

        return {
            "Base Color": base_color,
            "Complementary Palette": complementary,
            "Analogous Palette": analogous,
            "Triadic Palette": triadic,
            "Monochromatic Palette": monochromatic,
        }