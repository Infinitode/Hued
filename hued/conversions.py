"""
Module: conversions.py

This module provides methods for converting between different color formats,
including RGB, HEX, HSL, HSV, and CMYK.

Methods:
    - rgb_to_hex(r, g, b): Converts RGB to HEX.
    - hex_to_rgb(hex_value): Converts HEX to RGB.
    - rgb_to_hsl(r, g, b): Converts RGB to HSL.
    - hsl_to_rgb(h, s, l): Converts HSL to RGB.
    - rgb_to_hsv(r, g, b): Converts RGB to HSV.
    - hsv_to_rgb(h, s, v): Converts HSV to RGB.
    - rgb_to_cmyk(r, g, b): Converts RGB to CMYK.
    - cmyk_to_rgb(c, m, y, k): Converts CMYK to RGB.
"""

def rgb_to_hex(r, g, b):
    """
    Converts RGB values to a hex color code.

    Parameters:
        r (int): Red value (0-255).
        g (int): Green value (0-255).
        b (int): Blue value (0-255).

    Returns:
        str: A string representing the hex color code (e.g., "#FFFFFF").
    """
    return f"#{r:02X}{g:02X}{b:02X}"

def hex_to_rgb(hex_value):
    """
    Converts a hex color code to RGB values.

    Parameters:
        hex_value (str): A string representing a hex color code (e.g., "#FFFFFF").

    Returns:
        tuple: A tuple representing the RGB values (e.g., (255, 255, 255)).
    """
    hex_value = hex_value.lstrip('#')
    return tuple(int(hex_value[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hsl(r, g, b):
    """
    Converts RGB values to HSL (Hue, Saturation, Lightness).

    Parameters:
        r (int): Red value (0-255).
        g (int): Green value (0-255).
        b (int): Blue value (0-255).

    Returns:
        tuple: A tuple representing the HSL values (h, s, l) where
               h (float) is hue in the range [0, 360),
               s (float) is saturation in the range [0, 1],
               l (float) is lightness in the range [0, 1].
    """
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    max_c, min_c = max(r, g, b), min(r, g, b)
    delta = max_c - min_c
    l = (max_c + min_c) / 2

    if delta == 0:
        h = s = 0  # achromatic
    else:
        s = delta / (1 - abs(2 * l - 1))
        if max_c == r:
            h = ((g - b) / delta) % 6
        elif max_c == g:
            h = (b - r) / delta + 2
        elif max_c == b:
            h = (r - g) / delta + 4
        h *= 60

    return round(h, 2), round(s, 2), round(l, 2)

def hsl_to_rgb(h, s, l):
    """
    Converts HSL values to RGB.

    Parameters:
        h (float): Hue in the range [0, 360).
        s (float): Saturation in the range [0, 1].
        l (float): Lightness in the range [0, 1].

    Returns:
        tuple: A tuple representing the RGB values (0-255).
    """
    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c/2

    if 0 <= h < 60:
        r, g, b = c, x, 0
    elif 60 <= h < 120:
        r, g, b = x, c, 0
    elif 120 <= h < 180:
        r, g, b = 0, c, x
    elif 180 <= h < 240:
        r, g, b = 0, x, c
    elif 240 <= h < 300:
        r, g, b = x, 0, c
    elif 300 <= h < 360:
        r, g, b = c, 0, x
    else:
        r, g, b = 0, 0, 0

    return round((r + m) * 255), round((g + m) * 255), round((b + m) * 255)

def rgb_to_hsv(r, g, b):
    """
    Converts RGB values to HSV (Hue, Saturation, Value).

    Parameters:
        r (int): Red value (0-255).
        g (int): Green value (0-255).
        b (int): Blue value (0-255).

    Returns:
        tuple: A tuple representing the HSV values (h, s, v) where
               h (float) is hue in the range [0, 360),
               s (float) is saturation in the range [0, 1],
               v (float) is value in the range [0, 1].
    """
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    max_c, min_c = max(r, g, b), min(r, g, b)
    delta = max_c - min_c
    v = max_c

    if delta == 0:
        h = s = 0  # achromatic
    else:
        s = delta / max_c
        if max_c == r:
            h = ((g - b) / delta) % 6
        elif max_c == g:
            h = (b - r) / delta + 2
        elif max_c == b:
            h = (r - g) / delta + 4
        h *= 60

    return round(h, 2), round(s, 2), round(v, 2)

def hsv_to_rgb(h, s, v):
    """
    Converts HSV values to RGB.

    Parameters:
        h (float): Hue in the range [0, 360).
        s (float): Saturation in the range [0, 1].
        v (float): Value in the range [0, 1].

    Returns:
        tuple: A tuple representing the RGB values (0-255).
    """
    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c

    if 0 <= h < 60:
        r, g, b = c, x, 0
    elif 60 <= h < 120:
        r, g, b = x, c, 0
    elif 120 <= h < 180:
        r, g, b = 0, c, x
    elif 180 <= h < 240:
        r, g, b = 0, x, c
    elif 240 <= h < 300:
        r, g, b = x, 0, c
    elif 300 <= h < 360:
        r, g, b = c, 0, x
    else:
        r, g, b = 0, 0, 0

    return round((r + m) * 255), round((g + m) * 255), round((b + m) * 255)

def rgb_to_cmyk(r, g, b):
    """
    Converts RGB values to CMYK (Cyan, Magenta, Yellow, Key/Black).

    Parameters:
        r (int): Red value (0-255).
        g (int): Green value (0-255).
        b (int): Blue value (0-255).

    Returns:
        tuple: A tuple representing the CMYK values (c, m, y, k) where
               c (float) is cyan in the range [0, 1],
               m (float) is magenta in the range [0, 1],
               y (float) is yellow in the range [0, 1],
               k (float) is key/black in the range [0, 1].
    """
    if (r, g, b) == (0, 0, 0):
        return 0, 0, 0, 1

    c = 1 - r / 255.0
    m = 1 - g / 255.0
    y = 1 - b / 255.0
    k = min(c, m, y)

    c = (c - k) / (1 - k)
    m = (m - k) / (1 - k)
    y = (y - k) / (1 - k)

    return round(c, 2), round(m, 2), round(y, 2), round(k, 2)

def cmyk_to_rgb(c, m, y, k):
    """
    Converts CMYK values to RGB.

    Parameters:
        c (float): Cyan in the range [0, 1].
        m (float): Magenta in the range [0, 1].
        y (float): Yellow in the range [0, 1].
        k (float): Key/black in the range [0, 1].

    Returns:
        tuple: A tuple representing the RGB values (0-255).
    """
    r = 255 * (1 - c) * (1 - k)
    g = 255 * (1 - m) * (1 - k)
    b = 255 * (1 - y) * (1 - k)

    return round(r), round(g), round(b)

def hex_to_hsl(hex_value: str) -> tuple:
    """
    Converts a hex color code to HSL (Hue, Saturation, Lightness).

    Parameters:
        hex_value (str): A string representing a hex color code (e.g., "#FFFFFF").

    Returns:
        tuple: A tuple representing the HSL values (h, s, l) where
               h (float) is hue in the range [0, 360),
               s (float) is saturation in the range [0, 1],
               l (float) is lightness in the range [0, 1].
    """
    rgb = hex_to_rgb(hex_value)
    return rgb_to_hsl(*rgb)

def hex_to_hsv(hex_value: str) -> tuple:
    """
    Converts a hex color code to HSV (Hue, Saturation, Value).

    Parameters:
        hex_value (str): A string representing a hex color code (e.g., "#FFFFFF").

    Returns:
        tuple: A tuple representing the HSV values (h, s, v) where
               h (float) is hue in the range [0, 360),
               s (float) is saturation in the range [0, 1],
               v (float) is value in the range [0, 1].
    """
    rgb = hex_to_rgb(hex_value)
    return rgb_to_hsv(*rgb)

def hex_to_cmyk(hex_value: str) -> tuple:
    """
    Converts a hex color code to CMYK (Cyan, Magenta, Yellow, Key/Black).

    Parameters:
        hex_value (str): A string representing a hex color code (e.g., "#FFFFFF").

    Returns:
        tuple: A tuple representing the CMYK values (c, m, y, k) where
               c (float) is cyan in the range [0, 1],
               m (float) is magenta in the range [0, 1],
               y (float) is yellow in the range [0, 1],
               k (float) is key/black in the range [0, 1].
    """
    rgb = hex_to_rgb(hex_value)
    return rgb_to_cmyk(*rgb)

def hsl_to_hex(hsl_value: tuple) -> str:
    """
    Converts HSL (Hue, Saturation, Lightness) to a hex color code.

    Parameters:
        hsl_value (tuple): A tuple representing the HSL values (h, s, l) where
                           h (float) is hue in the range [0, 360),
                           s (float) is saturation in the range [0, 1],
                           l (float) is lightness in the range [0, 1].

    Returns:
        str: A string representing the hex color code (e.g., "#FFFFFF").

    Raises:
        ValueError: If the HSL values are out of range.
    """
    h, s, l = hsl_value
    if not (0 <= h < 360 and 0 <= s <= 1 and 0 <= l <= 1):
        raise ValueError("HSL values must be in range: h [0, 360), s [0, 1], l [0, 1]")

    return rgb_to_hex(*hsl_to_rgb(h, s, l))

def hsl_to_hsv(hsl_value: tuple) -> tuple:
    """
    Converts HSL (Hue, Saturation, Lightness) to HSV (Hue, Saturation, Value).

    Parameters:
        hsl_value (tuple): A tuple representing the HSL values (h, s, l) where
                           h (float) is hue in the range [0, 360),
                           s (float) is saturation in the range [0, 1],
                           l (float) is lightness in the range [0, 1].

    Returns:
        tuple: A tuple representing the HSV values (h, s, v) where
               h (float) is hue in the range [0, 360),
               s (float) is saturation in the range [0, 1],
               v (float) is value in the range [0, 1].

    Raises:
        ValueError: If the HSL values are out of range.
    """
    h, s, l = hsl_value
    if not (0 <= h < 360 and 0 <= s <= 1 and 0 <= l <= 1):
        raise ValueError("HSL values must be in range: h [0, 360), s [0, 1], l [0, 1]")

    return rgb_to_hsv(*hsl_to_rgb(h, s, l))

def hsl_to_cmyk(hsl_value: tuple) -> tuple:
    """
    Converts HSL (Hue, Saturation, Lightness) to CMYK (Cyan, Magenta, Yellow, Key/Black).

    Parameters:
        hsl_value (tuple): A tuple representing the HSL values (h, s, l) where
                           h (float) is hue in the range [0, 360),
                           s (float) is saturation in the range [0, 1],
                           l (float) is lightness in the range [0, 1].

    Returns:
        tuple: A tuple representing the CMYK values (c, m, y, k) where
               c (float) is cyan in the range [0, 1],
               m (float) is magenta in the range [0, 1],
               y (float) is yellow in the range [0, 1],
               k (float) is key/black in the range [0, 1].

    Raises:
        ValueError: If the HSL values are out of range.
    """
    h, s, l = hsl_value
    if not (0 <= h < 360 and 0 <= s <= 1 and 0 <= l <= 1):
        raise ValueError("HSL values must be in range: h [0, 360), s [0, 1], l [0, 1]")

    return rgb_to_cmyk(*hsl_to_rgb(h, s, l))

def hsv_to_hex(hsv_value: tuple) -> str:
    """
    Converts HSV (Hue, Saturation, Value) to a hex color code.

    Parameters:
        hsv_value (tuple): A tuple representing the HSV values (h, s, v) where
                           h (float) is hue in the range [0, 360),
                           s (float) is saturation in the range [0, 1],
                           v (float) is value in the range [0, 1].

    Returns:
        str: A string representing the hex color code (e.g., "#FFFFFF").

    Raises:
        ValueError: If the HSV values are out of range.
    """
    h, s, v = hsv_value
    if not (0 <= h < 360 and 0 <= s <= 1 and 0 <= v <= 1):
        raise ValueError("HSV values must be in range: h [0, 360), s [0, 1], v [0, 1]")

    return rgb_to_hex(*hsv_to_rgb(h, s, v))

def hsv_to_hsl(hsv_value: tuple) -> tuple:
    """
    Converts HSV (Hue, Saturation, Value) to HSL (Hue, Saturation, Lightness).

    Parameters:
        hsv_value (tuple): A tuple representing the HSV values (h, s, v) where
                           h (float) is hue in the range [0, 360),
                           s (float) is saturation in the range [0, 1],
                           v (float) is value in the range [0, 1].

    Returns:
        tuple: A tuple representing the HSL values (h, s, l) where
               h (float) is hue in the range [0, 360),
               s (float) is saturation in the range [0, 1],
               l (float) is lightness in the range [0, 1].

    Raises:
        ValueError: If the HSV values are out of range.
    """
    h, s, v = hsv_value
    if not (0 <= h < 360 and 0 <= s <= 1 and 0 <= v <= 1):
        raise ValueError("HSV values must be in range: h [0, 360), s [0, 1], v [0, 1]")

    return rgb_to_hsl(*hsv_to_rgb(h, s, v))

def hsv_to_cmyk(hsv_value: tuple) -> tuple:
    """
    Converts HSV (Hue, Saturation, Value) to CMYK (Cyan, Magenta, Yellow, Key/Black).

    Parameters:
        hsv_value (tuple): A tuple representing the HSV values (h, s, v) where
                           h (float) is hue in the range [0, 360),
                           s (float) is saturation in the range [0, 1],
                           v (float) is value in the range [0, 1].

    Returns:
        tuple: A tuple representing the CMYK values (c, m, y, k) where
               c (float) is cyan in the range [0, 1],
               m (float) is magenta in the range [0, 1],
               y (float) is yellow in the range [0, 1],
               k (float) is key/black in the range [0, 1].

    Raises:
        ValueError: If the HSV values are out of range.
    """
    h, s, v = hsv_value
    if not (0 <= h < 360 and 0 <= s <= 1 and 0 <= v <= 1):
        raise ValueError("HSV values must be in range: h [0, 360), s [0, 1], v [0, 1]")

    return rgb_to_cmyk(*hsv_to_rgb(h, s, v))

def cmyk_to_hex(cmyk_value: tuple) -> str:
    """
    Converts CMYK (Cyan, Magenta, Yellow, Key/Black) to a hex color code.

    Parameters:
        cmyk_value (tuple): A tuple representing the CMYK values (c, m, y, k) where
                            c (float) is cyan in the range [0, 1],
                            m (float) is magenta in the range [0, 1],
                            y (float) is yellow in the range [0, 1],
                            k (float) is key/black in the range [0, 1].

    Returns:
        str: A string representing the hex color code (e.g., "#FFFFFF").

    Raises:
        ValueError: If the CMYK values are out of range.
    """
    c, m, y, k = cmyk_value
    if not (0 <= c <= 1 and 0 <= m <= 1 and 0 <= y <= 1 and 0 <= k <= 1):
        raise ValueError("CMYK values must be in range: c, m, y, k [0, 1]")

    return rgb_to_hex(*cmyk_to_rgb(c, m, y, k))

def cmyk_to_hsv(cmyk_value: tuple) -> tuple:
    """
    Converts CMYK (Cyan, Magenta, Yellow, Key/Black) to HSV (Hue, Saturation, Value).

    Parameters:
        cmyk_value (tuple): A tuple representing the CMYK values (c, m, y, k) where
                            c (float) is cyan in the range [0, 1],
                            m (float) is magenta in the range [0, 1],
                            y (float) is yellow in the range [0, 1],
                            k (float) is key/black in the range [0, 1].

    Returns:
        tuple: A tuple representing the HSV values (h, s, v) where
               h (float) is hue in the range [0, 360),
               s (float) is saturation in the range [0, 1],
               v (float) is value in the range [0, 1].

    Raises:
        ValueError: If the CMYK values are out of range.
    """
    c, m, y, k = cmyk_value
    if not (0 <= c <= 1 and 0 <= m <= 1 and 0 <= y <= 1 and 0 <= k <= 1):
        raise ValueError("CMYK values must be in range: c, m, y, k [0, 1]")

    return rgb_to_hsv(*cmyk_to_rgb(c, m, y, k))

def cmyk_to_hsl(cmyk_value: tuple) -> tuple:
    """
    Converts CMYK (Cyan, Magenta, Yellow, Key/Black) to HSL (Hue, Saturation, Lightness).

    Parameters:
        cmyk_value (tuple): A tuple representing the CMYK values (c, m, y, k) where
                            c (float) is cyan in the range [0, 1],
                            m (float) is magenta in the range [0, 1],
                            y (float) is yellow in the range [0, 1],
                            k (float) is key/black in the range [0, 1].

    Returns:
        tuple: A tuple representing the HSL values (h, s, l) where
               h (float) is hue in the range [0, 360),
               s (float) is saturation in the range [0, 1],
               l (float) is lightness in the range [0, 1].

    Raises:
        ValueError: If the CMYK values are out of range.
    """
    c, m, y, k = cmyk_value
    if not (0 <= c <= 1 and 0 <= m <= 1 and 0 <= y <= 1 and 0 <= k <= 1):
        raise ValueError("CMYK values must be in range: c, m, y, k [0, 1]")

    return rgb_to_hsl(*cmyk_to_rgb(c, m, y, k))

def blend_colors(color1, color2, ratio=0.5):
    """
    Blends two colors in the RGB format using the specified ratio.

    This function takes two RGB colors and blends them based on the provided ratio.
    A ratio of 0.5 will give an equal mix of both colors, while other ratios will
    give more weight to one color over the other.

    Parameters:
        color1 (tuple): The first RGB color as a tuple of three integers (R, G, B).
        color2 (tuple): The second RGB color as a tuple of three integers (R, G, B).
        ratio (float, optional): The ratio to blend the colors. A value of 0.5 will
                                 blend both colors equally. Values closer to 0 will
                                 give more weight to `color1`, and values closer to
                                 1 will favor `color2`. Default is 0.5.

    Returns:
        tuple: The blended color as an RGB tuple of three integers.

    Example:
        >>> blend_colors((255, 0, 0), (0, 0, 255), 0.5)
        (127, 0, 127)
    """
    r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
    g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
    b = int(color1[2] * (1 - ratio) + color2[2] * ratio)

    return (r, g, b)