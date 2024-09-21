# Hued
![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)
![Code Size](https://img.shields.io/github/languages/code-size/infinitode/hued)
![Downloads](https://pepy.tech/badge/hued)
![License Compliance](https://img.shields.io/badge/license-compliance-brightgreen.svg)
![PyPI Version](https://img.shields.io/pypi/v/hued)

An open-source Python library for color generation, conversion, and retrieval of common properties, palettes, and color information.

## Installation

You can install Hued using pip:

```bash
pip install hued
```

## Supported Python Versions

Hued supports the following Python versions:

- Python 3.6
- Python 3.7
- Python 3.8
- Python 3.9
- Python 3.10
- Python 3.11 or later

Please ensure that one of these Python versions is installed before using Hued. Hued may not work as expected on lower versions of Python than the supported.

## Features

- Color Generation: Generate random colors and palettes.
- Color Conversion: Convert between different color formats (RGB, HEX, HSL, etc.).
- Color Properties: Retrieve properties like brightness, temperature, and whether a color is muted, pastel, or vibrant.
- Color Names: Get relevant color names, based on HEX values, and convert between color names and HEX values.

## Usage

### Color Properties

```python
from hued.colors import ColorManager

# Initialize the color manager
color_manager = ColorManager()

# Generate a random color
colorBlue = color_manager.get_color_by_name("Blue");

print("Blue Hex:", colorBlue.get("Hex"));
```

> You can view more properties by going to Hued's [package documentation](https://infinitode-docs.gitbook.io/documentation/package-documentation/hued-package-documentation)

### Color Conversion

```python
from hued.conversions import hex_to_rgb, rgb_to_hsl

# Convert HEX to RGB
rgb_color = hex_to_rgb("FF0000"); # Red
print(f"Hex to RGB: {rgb_color}")

# Convert RGB to HSL
hsl_color = rgb_to_hsl(255, 0, 0) # Red
print(f"RGB to HSL: {hsl_color}")
```

### Color Analysis

```python
from hued.analysis import get_temperature, is_pastel

# Check if a color is a pastel color
pastel_color = (255, 200, 200)  # Example pastel color
is_pastel = is_pastel(pastel_color)
print(f"Is Pastel: {is_pastel}")

# Check if a color is vibrant
warm_color = (255, 0, 0)  # Example warm color
temperature = get_temperature(warm_color)
print(f"The current color is: {temperature}") # Warm
```

### Color Generation and Palettes

```python
from hued.palettes import ColorPalette

base_color = (255, 60, 52)  # Red

# Initialize the ColorPalette with a base color (RGB)
palette = ColorPalette(base_color)

# Get the complementary color
complementary = palette.generate_complementary()
print(f"Complementary color of {base_color}: {complementary}")

# Generate a random palette, with calculated color schemes, and base color
random_palette = palette.generate_random_palette()
print(f"Generated color palette's base color: {random_palette.get('Base Color')}")
```

> More functions are available for the `ColorPalette` class, including converting all contained colors to **Hex colors**.

## Contributing

Contributions are welcome! If you encounter any issues, have suggestions, or want to contribute to Hued, please open an issue or submit a pull request on [GitHub](https://github.com/infinitode/hued).

## License

Hued is released under the terms of the **MIT License (Modified)**. Please see the [LICENSE](https://github.com/infinitode/hued/blob/main/LICENSE) file for the full text.

**Modified License Clause**

The modified license clause grants users the permission to make derivative works based on the Hued software. However, it requires any substantial changes to the software to be clearly distinguished from the original work and distributed under a different name.

By enforcing this distinction, it aims to prevent direct publishing of the source code without changes while allowing users to create derivative works that incorporate the code but are not exactly the same.

Please read the full license terms in the [LICENSE](https://github.com/infinitode/hued/blob/main/LICENSE) file for complete details.
