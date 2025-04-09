import random
import json
import csv
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

    def generate_random_palette(self, set_as_current=True):
        """
        Generates a random base color and its associated palettes as a dictionary.

        Parameters:
            set_as_current (bool): If True, sets self.palette to the generated dictionary.
                                   If False, returns the dictionary without modifying self.palette.

        Returns:
            dict: A dictionary containing the base color and various generated palettes (as lists of RGB tuples).
                  Example keys: 'Base Color', 'Complementary Palette', 'Analogous Palette', etc.
        """
        # Generate a random RGB color
        random_base_color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )

        # Store current state
        original_base = self.base_color
        original_palette = self.palette

        # Temporarily set base color for generation
        self.base_color = random_base_color

        # Generate the palettes using the instance methods
        # These methods currently modify self.palette, so we capture their return value
        palette_dict = {
            "Base Color": random_base_color, # Store the base color itself
            "Complementary Palette": self.generate_complementary(),
            "Analogous Palette": self.generate_analogous(),
            "Triadic Palette": self.generate_triadic(),
            "Monochromatic Palette": self.generate_monochromatic(),
            "Tetradic Palette": self.generate_tetradic(),
            "Square Palette": self.generate_square(), # Often same as tetradic here
            "Split Complementary Palette": self.generate_split_complementary()
        }

        # Restore original state or set the new dict as the current palette
        if set_as_current:
            self.palette = palette_dict
            # self.base_color remains the random_base_color in this case
        else:
            self.base_color = original_base
            self.palette = original_palette

        return palette_dict

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

    def generate_gradient(self, color1, color2, steps=10):
        """
        Generates a gradient between two RGB colors.

        Parameters:
            color1 (tuple): The starting RGB color (0-255).
            color2 (tuple): The ending RGB color (0-255).
            steps (int): The number of intermediate steps in the gradient (total colors = steps + 1).

        Returns:
            list: A list of RGB tuples representing the gradient.
                  Does NOT modify self.palette.
        """
        if steps < 1:
             raise ValueError("Number of steps must be at least 1.")
        gradient = []
        for i in range(steps + 1):
            ratio = i / steps
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            # Clamp values just in case of floating point inaccuracies
            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))
            gradient.append((r, g, b))
        return gradient

    def _format_color_output(self, color_tuple):
        """Helper to consistently format color output."""
        hex_val = rgb_to_hex(*color_tuple).upper()
        return {"rgb": color_tuple, "hex": hex_val}

    def export_palette(self, filename="palette.json"):
        """
        Exports the current color palette (list or dict) to a file.

        Handles both list-based palettes and dictionary-based palettes
        (like those from `generate_random_palette`).

        Supported formats: .json, .txt, .csv.

        - JSON: Exports the full structure, converting RGB tuples to
                {"rgb": (r,g,b), "hex": "#RRGGBB"} objects for clarity.
        - TXT:  Exports a human-readable text format, labeling each
                palette type if the source is a dictionary.
        - CSV:  Exports a flattened structure.
                For lists: Type, Index, Hex, R, G, B
                For dicts: PaletteName, Index, Hex, R, G, B

        Parameters:
            filename (str): The name of the file to save the palette.
                            The extension determines the format (.json, .txt, .csv).
                            Defaults to "palette.json".

        Raises:
            ValueError: If the filename has an unsupported extension or if
                        the palette is empty or in an unexpected format.
            TypeError: If self.palette is not a list or dict.
        """
        if not self.palette:
            raise ValueError("Palette is empty, cannot export.")

        file_ext = filename.lower().split('.')[-1]

        try:
            if isinstance(self.palette, list):
                # --- Handle List Palette Export ---
                if file_ext == "json":
                    export_data = [self._format_color_output(color) for color in self.palette]
                    with open(filename, "w", encoding='utf-8') as f:
                        json.dump(export_data, f, indent=4)
                elif file_ext == "txt":
                    with open(filename, "w", encoding='utf-8') as f:
                        f.write("--- Simple Palette ---\n")
                        for i, color in enumerate(self.palette):
                            formatted = self._format_color_output(color)
                            f.write(f"{i}: {formatted['hex']} - RGB{formatted['rgb']}\n")
                elif file_ext == "csv":
                    with open(filename, "w", newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerow(["Type", "Index", "Hex", "R", "G", "B"])
                        for i, color in enumerate(self.palette):
                            formatted = self._format_color_output(color)
                            writer.writerow(["Simple Palette", i, formatted['hex'], color[0], color[1], color[2]])
                else:
                    raise ValueError("Unsupported file format. Use .json, .txt, or .csv.")

            elif isinstance(self.palette, dict):
                # --- Handle Dictionary Palette Export ---
                if file_ext == "json":
                    export_data = {}
                    for key, value in self.palette.items():
                        if isinstance(value, tuple) and len(value) == 3: # Single color
                            export_data[key] = self._format_color_output(value)
                        elif isinstance(value, list): # List of colors
                            export_data[key] = [self._format_color_output(color) for color in value]
                        else:
                            export_data[key] = value # Preserve other data types
                    with open(filename, "w", encoding='utf-8') as f:
                        json.dump(export_data, f, indent=4)
                elif file_ext == "txt":
                    with open(filename, "w", encoding='utf-8') as f:
                        for key, value in self.palette.items():
                            f.write(f"--- {key} ---\n")
                            if isinstance(value, tuple) and len(value) == 3: # Single color
                                formatted = self._format_color_output(value)
                                f.write(f"0: {formatted['hex']} - RGB{formatted['rgb']}\n")
                            elif isinstance(value, list): # List of colors
                                for i, color in enumerate(value):
                                    formatted = self._format_color_output(color)
                                    f.write(f"{i}: {formatted['hex']} - RGB{formatted['rgb']}\n")
                            else:
                                f.write(f"{value}\n") # Write other data as is
                            f.write("\n") # Add space between sections
                elif file_ext == "csv":
                    with open(filename, "w", newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerow(["PaletteName", "Index", "Hex", "R", "G", "B"])
                        for key, value in self.palette.items():
                            if isinstance(value, tuple) and len(value) == 3: # Single color
                                formatted = self._format_color_output(value)
                                writer.writerow([key, 0, formatted['hex'], value[0], value[1], value[2]])
                            elif isinstance(value, list): # List of colors
                                for i, color in enumerate(value):
                                    formatted = self._format_color_output(color)
                                    writer.writerow([key, i, formatted['hex'], color[0], color[1], color[2]])
                            # Ignoring non-color list/tuple values for CSV
                else:
                    raise ValueError("Unsupported file format. Use .json, .txt, or .csv.")
            else:
                raise TypeError(f"Unsupported palette type: {type(self.palette)}. Must be list or dict.")

        except IOError as e:
            print(f"Error writing to file {filename}: {e}")
            raise # Re-raise the exception after printing
        except Exception as e:
            print(f"An unexpected error occurred during export: {e}")
            raise # Re-raise