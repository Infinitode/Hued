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
            shades (int): Number of shades to generate (default 24).

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

    def generate_tetradic(self):
        """
        Generates a tetradic color palette.

        Returns:
            list: A list of RGB tuples representing the tetradic palette.
        """
        h, s, l = rgb_to_hsl(*self.base_color)
        tetradic1_h = (h + 90) % 360
        tetradic2_h = (h + 180) % 360
        tetradic3_h = (h + 270) % 360

        tetradic1 = hsl_to_rgb(tetradic1_h, s, l)
        tetradic2 = hsl_to_rgb(tetradic2_h, s, l)
        tetradic3 = hsl_to_rgb(tetradic3_h, s, l)

        self.palette = [self.base_color, tetradic1, tetradic2, tetradic3]
        return self.palette

    def generate_square(self):
        """
        Generates a square color palette.

        Returns:
            list: A list of RGB tuples representing the square palette.
        """
        h, s, l = rgb_to_hsl(*self.base_color)
        square1_h = (h + 90) % 360
        square2_h = (h + 180) % 360
        square3_h = (h + 270) % 360

        square1 = hsl_to_rgb(square1_h, s, l)
        square2 = hsl_to_rgb(square2_h, s, l)
        square3 = hsl_to_rgb(square3_h, s, l)

        self.palette = [self.base_color, square1, square2, square3]
        return self.palette

    def generate_split_complementary(self):
        """
        Generates a split-complementary color palette.

        Returns:
            list: A list of RGB tuples representing the split-complementary palette.
        """
        h, s, l = rgb_to_hsl(*self.base_color)
        split_comp1_h = (h + 150) % 360
        split_comp2_h = (h + 210) % 360

        split_comp1 = hsl_to_rgb(split_comp1_h, s, l)
        split_comp2 = hsl_to_rgb(split_comp2_h, s, l)

        self.palette = [self.base_color, split_comp1, split_comp2]
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
        """
        Generates a random base color and its associated palettes.

        Returns:
            dict: A dictionary containing the following keys:
                - 'Base Color' (tuple): The randomly generated RGB base color, e.g., (R, G, B).
                - 'Complementary Palette' (list): A list of colors in the complementary palette.
                - 'Analogous Palette' (list): A list of colors in the analogous palette.
                - 'Triadic Palette' (list): A list of colors in the triadic palette.
                - 'Monochromatic Palette' (list): A list of colors in the monochromatic palette.
        """

        # Generate a random RGB color
        base_color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )

        self.base_color = base_color

        # Generate the palettes
        complementary = self.generate_complementary()
        analogous = self.generate_analogous()
        triadic = self.generate_triadic()
        monochromatic = self.generate_monochromatic()
        tetradic = self.generate_tetradic()
        square = self.generate_square()
        split_complementary = self.generate_split_complementary()

        return {
            "Base Color": base_color,
            "Complementary Palette": complementary,
            "Analogous Palette": analogous,
            "Triadic Palette": triadic,
            "Monochromatic Palette": monochromatic,
            "Tetradic Palette": tetradic,
            "Square Palette": square,
            "Split Complementary Palette": split_complementary
        }

    def generate_random_color(self):
        """
        Generates a random RGB color and converts it to both HEX and HSL formats.

        This method generates a random color in the RGB format by selecting random
        values for red, green, and blue channels between 0 and 255. It then converts
        the generated RGB values into both HEX and HSL formats.

        Returns:
            dict: A dictionary containing:
                - "RGB Color" (tuple): The random RGB color as a tuple of three integers.
                - "HEX Color" (str): The color converted into HEX format.
                - "HSL Color" (tuple): The color converted into HSL format.
        """

        # Generate a random RGB color
        base_color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )

        hex_color = rgb_to_hex(base_color[0], base_color[1], base_color[2])
        hsl_color = rgb_to_hsl(base_color[0], base_color[1], base_color[2])

        return {
            "RGB Color": base_color,
            "HEX Color": hex_color,
            "HSL Color": hsl_color
        }

    def generate_random_hex_colors(self, n=10):
        """
        Generates a list of random colors in HEX format.

        This method uses `generate_random_color` to generate multiple random colors
        and extracts the HEX value of each color. By default, it generates 10 random
        HEX colors.

        Parameters:
            n (int, optional): The number of random HEX colors to generate. Default is 10.

        Returns:
            list: A list of HEX color strings.
        """

        hex_colors = []
        for i in range(n):
            hex_color = self.generate_random_color().get("HEX Color")
            hex_colors.append(hex_color)

        return hex_colors