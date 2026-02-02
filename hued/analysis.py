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

def rgb_to_linear(rgb):
    """Convert RGB values to linear RGB.

    The input RGB values should be in the range [0, 255]. This function
    applies the sRGB transfer function to convert each RGB component
    to its linear equivalent, which is useful for various color
    calculations, including luminance and color mixing.

    Parameters:
        rgb (tuple): A tuple of three integers representing the RGB
                     values (r, g, b), each in the range [0, 255].

    Returns:
        list: A list of three floats representing the linear RGB values.
    """
    r, g, b = rgb
    return [
        (c / 255) ** 2.2 if c > 0.04045 else c / 255 / 12.92 for c in (r, g, b)
    ]

def get_luminance(rgb):
    """Calculate the relative luminance of an RGB color.

    This function converts the input RGB color to linear RGB and
    then computes the relative luminance using the standard
    formula based on the RGB color's linear components.
    The coefficients used are based on the sRGB color space.

    Parameters:
        rgb (tuple): A tuple of three integers representing the RGB
                     values (r, g, b), each in the range [0, 255].

    Returns:
        float: The calculated relative luminance of the RGB color.
    """
    r_linear, g_linear, b_linear = rgb_to_linear(rgb)
    return 0.2126 * r_linear + 0.7152 * g_linear + 0.0722 * b_linear

def get_vibrancy(rgb):
    """Calculate the vibrancy of an RGB color.

    This function computes vibrancy based on the chromaticity of the RGB values.
    A higher value indicates a more vibrant color.

    Parameters:
        rgb (tuple): A tuple of three integers representing the RGB
                     values (r, g, b), each in the range [0, 255].

    Returns:
        float: The calculated vibrancy of the RGB color.
    """
    r, g, b = rgb
    max_color = max(r, g, b)
    min_color = min(r, g, b)
    if max_color == 0:
        return 0  # Avoid division by zero; neutral color

    vibrancy = (max_color - min_color) / max_color  # A simple measure of vibrancy
    return vibrancy

def color_contrast(color1, color2):
    """
    Calculates the contrast ratio between two colors using their RGB values.

    The contrast ratio is calculated based on the relative luminance of each color
    and is used to determine the readability of text on different background colors.
    The result is a number between 1 and 21, where a higher value indicates better
    contrast.

    Parameters:
        color1 (tuple): The first RGB color as a tuple of three integers (R, G, B).
        color2 (tuple): The second RGB color as a tuple of three integers (R, G, B).

    Returns:
        float: The contrast ratio between the two colors.
    """

    L1 = get_luminance(color1)
    L2 = get_luminance(color2)
    if L1 > L2:
        return (L1 + 0.05) / (L2 + 0.05)
    else:
        return (L2 + 0.05) / (L1 + 0.05)

def get_text_color_from_background(background_color):
    """Determines whether the text should be "light" or "dark" based on the background color.

    Parameters:
        background_color (tuple): The background RGB color as a tuple of three integers (R, G, B).

    Returns:
        str: "light" if the background is dark and vibrant, "dark" if the background is bright and muted.
    """
    # Calculate luminance and vibrancy of the background color
    luminance_value = get_luminance(background_color)
    vibrancy_value = get_vibrancy(background_color)

    # Enhanced decision logic based on luminance and vibrancy
    if luminance_value < 0.3:  # Dark background
        if vibrancy_value > 0.4:  # Vibrant dark colors
            return "light"  # Use light text for better readability
        else:
            return "dark"  # Use dark text if it's a muted dark color
    elif luminance_value < 0.6:  # Medium background (transition zone)
        if vibrancy_value > 0.5:  # Bright but vibrant
            return "dark"  # Use dark text for readability
        else:
            return "light"  # Use light text if the color is less vibrant
    else:  # Bright background
        if vibrancy_value < 0.4:  # Muted bright colors
            return "dark"  # Use dark text for readability
        else:
            return "light"  # Use light text for vibrant bright colors

def check_color_quality(rgb):
    """
    Evaluates if a color is of 'good quality' for UI/text usage.

    This function simulates a color visibility tester by checking the color's
    contrast ratio against standard black and white backgrounds. A color is
    considered 'good quality' if it meets the WCAG AA standard (contrast ratio >= 4.5)
    against at least one of the backgrounds.

    Parameters:
        rgb (tuple): A tuple containing the RGB values (r, g, b).

    Returns:
        dict: A dictionary containing:
            - 'contrast_with_black' (float): Contrast ratio with black.
            - 'contrast_with_white' (float): Contrast ratio with white.
            - 'is_good_quality' (bool): True if legible on black or white.
    """
    black = (0, 0, 0)
    white = (255, 255, 255)

    contrast_black = color_contrast(rgb, black)
    contrast_white = color_contrast(rgb, white)

    # WCAG AA requires 4.5:1 for normal text
    is_good = contrast_black >= 4.5 or contrast_white >= 4.5

    return {
        "contrast_with_black": round(contrast_black, 2),
        "contrast_with_white": round(contrast_white, 2),
        "is_good_quality": is_good
    }

def simulate_color_blindness(rgb, blindness_type="protanopia", intensity=1.0):
    """
    Simulates color blindness on a given RGB color.

    Parameters:
        rgb (tuple): A tuple containing the RGB values (r, g, b).
        blindness_type (str): The type of color blindness to simulate.
                              Options: 'protanopia', 'deuteranopia', 'tritanopia', 'achromatopsia'.
                              Default is 'protanopia'.
        intensity (float): The intensity of the simulation (0.0 to 1.0).
                           Default is 1.0 (full simulation).

    Returns:
        tuple: A tuple representing the simulated RGB values.
    """
    if not (0 <= intensity <= 1):
        raise ValueError("Intensity must be between 0 and 1.")

    blindness_type = blindness_type.lower()

    # Matrices for color blindness simulation (approximate for sRGB/Linear)
    matrices = {
        "protanopia": [[0.567, 0.433, 0.0], [0.558, 0.442, 0.0], [0.0, 0.242, 0.758]],
        "deuteranopia": [[0.625, 0.375, 0.0], [0.7, 0.3, 0.0], [0.0, 0.3, 0.7]],
        "tritanopia": [[0.95, 0.05, 0.0], [0.0, 0.433, 0.567], [0.0, 0.475, 0.525]],
        "achromatopsia": [[0.299, 0.587, 0.114], [0.299, 0.587, 0.114], [0.299, 0.587, 0.114]]
    }

    if blindness_type not in matrices:
        raise ValueError(f"Unknown blindness type: {blindness_type}")

    matrix = matrices[blindness_type]
    r_lin, g_lin, b_lin = rgb_to_linear(rgb)

    r_sim = r_lin * matrix[0][0] + g_lin * matrix[0][1] + b_lin * matrix[0][2]
    g_sim = r_lin * matrix[1][0] + g_lin * matrix[1][1] + b_lin * matrix[1][2]
    b_sim = r_lin * matrix[2][0] + g_lin * matrix[2][1] + b_lin * matrix[2][2]

    # Convert back to sRGB (using simplified gamma 2.2 to match rgb_to_linear)
    def lin_to_srgb(c): return c ** (1 / 2.2)
    r_final, g_final, b_final = lin_to_srgb(max(0, r_sim)) * 255, lin_to_srgb(max(0, g_sim)) * 255, lin_to_srgb(max(0, b_sim)) * 255

    return (
        max(0, min(255, int(rgb[0] * (1 - intensity) + r_final * intensity))),
        max(0, min(255, int(rgb[1] * (1 - intensity) + g_final * intensity))),
        max(0, min(255, int(rgb[2] * (1 - intensity) + b_final * intensity)))
    )
    