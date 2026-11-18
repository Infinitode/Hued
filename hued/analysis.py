"""Color analysis, accessibility (WCAG 2.1), perceptual difference, and vision simulation."""

from __future__ import annotations

import math
from collections.abc import Sequence
from typing import Any

from hued.conversions import (
    _linear_to_srgb_channel,
    _rgb_to_hsl_exact,
    _rgb_to_hsv_exact,
    _srgb_to_linear_channel,
    _validate_real,
    _validate_rgb_number_tuple,
    rgb_to_lab,
)

__all__ = [
    "get_temperature",
    "is_neutral",
    "brightness",
    "is_pastel",
    "is_muted",
    "is_vibrant",
    "rgb_to_linear",
    "get_luminance",
    "get_vibrancy",
    "color_contrast",
    "check_wcag_contrast",
    "get_text_color_from_background",
    "check_color_quality",
    "simulate_color_blindness",
    "delta_e",
]

# Color-vision deficiency simulation matrices operating on linear sRGB.
# Row sums equal 1.0 so neutral grays preserve exact luminance.
_CVD_MATRICES: dict[str, tuple[tuple[float, float, float], ...]] = {
    "protanopia": (
        (0.567, 0.433, 0.0),
        (0.558, 0.442, 0.0),
        (0.0, 0.242, 0.758),
    ),
    "deuteranopia": (
        (0.625, 0.375, 0.0),
        (0.7, 0.3, 0.0),
        (0.0, 0.3, 0.7),
    ),
    "tritanopia": (
        (0.95, 0.05, 0.0),
        (0.0, 0.433, 0.567),
        (0.0, 0.475, 0.525),
    ),
    "achromatopsia": (
        (0.2126, 0.7152, 0.0722),
        (0.2126, 0.7152, 0.0722),
        (0.2126, 0.7152, 0.0722),
    ),
}


def get_temperature(rgb: Sequence[int]) -> str:
    """Classify the perceptual color temperature of an RGB color.

    Achromatic and very low-saturation colors return ``"Neutral"``. Chromatic
    colors are classified by hue into ``"Warm"`` (reds, oranges, yellows, and
    warm roses: ``0°–75°`` and ``330°–360°``), ``"Cool"`` (cool greens, teals,
    cyans, blues, and indigos: ``135°–270°``), or ``"Neutral"`` (transitional
    yellow-greens/greens and purples/magentas).

    Parameters:
        rgb (tuple): RGB color ``(r, g, b)`` in ``[0, 255]``.

    Returns:
        str: ``"Warm"``, ``"Cool"``, or ``"Neutral"``.
    """
    r, g, b = _validate_rgb_number_tuple(rgb)
    chroma = max(r, g, b) - min(r, g, b)
    h, s, _ = _rgb_to_hsv_exact(r, g, b)

    if chroma < 15.0 or s < 0.1:
        return "Neutral"
    if h <= 75.0 or h >= 330.0:
        return "Warm"
    if 135.0 <= h <= 270.0:
        return "Cool"
    return "Neutral"


def is_neutral(rgb: Sequence[int], tolerance: float = 30) -> bool:
    """Check whether an RGB color is neutral (near-gray).

    Parameters:
        rgb (tuple): RGB color ``(r, g, b)`` in ``[0, 255]``.
        tolerance (float): Exclusive maximum pairwise channel difference
            (default ``30``). Must be non-negative.

    Returns:
        bool: ``True`` if all pairwise channel differences are below ``tolerance``.
    """
    r, g, b = _validate_rgb_number_tuple(rgb)
    tol = _validate_real(tolerance, "tolerance")
    if tol < 0.0:
        raise ValueError(f"tolerance must be non-negative, got {tolerance}.")
    return abs(r - g) < tol and abs(g - b) < tol and abs(r - b) < tol


def brightness(rgb: Sequence[int]) -> float:
    """Calculate the perceived brightness (ITU-R BT.601 luma) of an RGB color.

    Parameters:
        rgb (tuple): RGB color ``(r, g, b)`` in ``[0, 255]``.

    Returns:
        float: Brightness value in ``[0.0, 1.0]``.
    """
    r, g, b = _validate_rgb_number_tuple(rgb)
    return (0.299 * r + 0.587 * g + 0.114 * b) / 255.0


def is_pastel(rgb: Sequence[int]) -> bool:
    """Check whether an RGB color is a pastel shade.

    Pastel colors combine high lightness/value with soft, non-zero saturation,
    excluding pure white, achromatic grays, dark shades, and vivid neons.

    Parameters:
        rgb (tuple): RGB color ``(r, g, b)`` in ``[0, 255]``.

    Returns:
        bool: ``True`` if the color is pastel, ``False`` otherwise.
    """
    r, g, b = _validate_rgb_number_tuple(rgb)
    _, s_hsv, v = _rgb_to_hsv_exact(r, g, b)
    _, _, l = _rgb_to_hsl_exact(r, g, b)
    return l >= 0.65 and v >= 0.75 and 0.05 <= s_hsv <= 0.55


def is_muted(rgb: Sequence[int]) -> bool:
    """Check whether an RGB color is muted (low saturation, mid/low brightness).

    Excludes pure/near-black and very bright shades (such as white and pastels).

    Parameters:
        rgb (tuple): RGB color ``(r, g, b)`` in ``[0, 255]``.

    Returns:
        bool: ``True`` if the color is muted, ``False`` otherwise.
    """
    r, g, b = _validate_rgb_number_tuple(rgb)
    luma = (0.299 * r + 0.587 * g + 0.114 * b) / 255.0
    _, s_hsv, _ = _rgb_to_hsv_exact(r, g, b)
    return 0.1 <= luma <= 0.75 and s_hsv < 0.5


def is_vibrant(rgb: Sequence[int]) -> bool:
    """Check whether an RGB color is vibrant (high HSV saturation and value).

    Parameters:
        rgb (tuple): RGB color ``(r, g, b)`` in ``[0, 255]``.

    Returns:
        bool: ``True`` if HSV saturation ``> 0.5`` and value ``> 0.7``.
    """
    r, g, b = _validate_rgb_number_tuple(rgb)
    _, s, v = _rgb_to_hsv_exact(r, g, b)
    return s > 0.5 and v > 0.7


def rgb_to_linear(rgb: Sequence[int]) -> list[float]:
    """Convert sRGB values ``[0, 255]`` to linear sRGB ``[0.0, 1.0]``.

    Applies the standard IEC 61966-2-1 / WCAG 2.1 sRGB inverse transfer
    function: ``s / 12.92`` for ``s <= 0.04045``, and
    ``((s + 0.055) / 1.055) ** 2.4`` otherwise, where ``s = c / 255``.

    Parameters:
        rgb (tuple): RGB color ``(r, g, b)`` in ``[0, 255]``.

    Returns:
        list[float]: Three linear RGB floats in ``[0.0, 1.0]``.
    """
    r, g, b = _validate_rgb_number_tuple(rgb)
    return [
        _srgb_to_linear_channel(r),
        _srgb_to_linear_channel(g),
        _srgb_to_linear_channel(b),
    ]


def get_luminance(rgb: Sequence[int]) -> float:
    """Calculate the WCAG 2.1 relative luminance of an sRGB color.

    Parameters:
        rgb (tuple): RGB color ``(r, g, b)`` in ``[0, 255]``.

    Returns:
        float: Relative luminance in ``[0.0, 1.0]`` (``0.0`` for black, ``1.0`` for white).
    """
    r_linear, g_linear, b_linear = rgb_to_linear(rgb)
    return 0.2126 * r_linear + 0.7152 * g_linear + 0.0722 * b_linear


def get_vibrancy(rgb: Sequence[int]) -> float:
    """Calculate the HSV chroma vibrancy ratio ``(max - min) / max`` of an RGB color.

    Parameters:
        rgb (tuple): RGB color ``(r, g, b)`` in ``[0, 255]``.

    Returns:
        float: Vibrancy score in ``[0.0, 1.0]``.
    """
    r, g, b = _validate_rgb_number_tuple(rgb)
    max_color = max(r, g, b)
    if max_color == 0.0:
        return 0.0
    min_color = min(r, g, b)
    return (max_color - min_color) / max_color


def color_contrast(color1: Sequence[int], color2: Sequence[int]) -> float:
    """Calculate the WCAG 2.1 contrast ratio between two RGB colors.

    Parameters:
        color1 (tuple): First RGB color ``(r, g, b)`` in ``[0, 255]``.
        color2 (tuple): Second RGB color ``(r, g, b)`` in ``[0, 255]``.

    Returns:
        float: Contrast ratio in ``[1.0, 21.0]`` (higher means stronger contrast).
    """
    l1 = get_luminance(color1)
    l2 = get_luminance(color2)
    lighter, darker = (l1, l2) if l1 >= l2 else (l2, l1)
    return (lighter + 0.05) / (darker + 0.05)


def check_wcag_contrast(
    foreground: Sequence[int],
    background: Sequence[int],
) -> dict[str, Any]:
    """Evaluate a foreground/background color pair against WCAG 2.1 thresholds.

    Parameters:
        foreground (tuple): Foreground/text RGB color ``(r, g, b)`` in ``[0, 255]``.
        background (tuple): Background RGB color ``(r, g, b)`` in ``[0, 255]``.

    Returns:
        dict: Dictionary containing:
            - ``contrast_ratio`` (float): Contrast ratio rounded to 2 decimals.
            - ``aa_normal`` (bool): Meets WCAG AA for normal text (``>= 4.5``).
            - ``aa_large`` (bool): Meets WCAG AA for large text (``>= 3.0``).
            - ``aaa_normal`` (bool): Meets WCAG AAA for normal text (``>= 7.0``).
            - ``aaa_large`` (bool): Meets WCAG AAA for large text (``>= 4.5``).
            - ``ui_components`` (bool): Meets WCAG AA for UI/graphics (``>= 3.0``).
    """
    ratio = color_contrast(foreground, background)
    return {
        "contrast_ratio": round(ratio, 2),
        "aa_normal": ratio >= 4.5,
        "aa_large": ratio >= 3.0,
        "aaa_normal": ratio >= 7.0,
        "aaa_large": ratio >= 4.5,
        "ui_components": ratio >= 3.0,
    }


def get_text_color_from_background(background_color: Sequence[int]) -> str:
    """Return ``"light"`` or ``"dark"`` text for maximum WCAG contrast on a background.

    Compares the WCAG 2.1 contrast ratio of pure white ``(255, 255, 255)`` and
    pure black ``(0, 0, 0)`` against ``background_color`` and picks whichever
    yields greater readability (equivalent to relative luminance threshold
    ``sqrt(1.05 * 0.05) - 0.05 ~= 0.1791``).

    Parameters:
        background_color (tuple): Background RGB color ``(r, g, b)`` in ``[0, 255]``.

    Returns:
        str: ``"light"`` when white text has higher contrast, otherwise ``"dark"``.
    """
    lum = get_luminance(background_color)
    contrast_with_white = 1.05 / (lum + 0.05)
    contrast_with_black = (lum + 0.05) / 0.05
    return "light" if contrast_with_white >= contrast_with_black else "dark"


def check_color_quality(
    rgb: Sequence[int],
    background: Sequence[int] | None = None,
    min_contrast: float | None = None,
) -> dict[str, Any]:
    """Evaluate a color's visibility and contrast quality for UI and text usage.

    Always computes contrast ratios and WCAG AA/AAA compliance against black
    ``(0, 0, 0)`` and white ``(255, 255, 255)``.

    Note:
        For any color, ``contrast_with_black * contrast_with_white == 21``, so
        ``max(contrast_with_black, contrast_with_white) >= sqrt(21) ~= 4.58``.
        Because a 4.5 threshold against "black or white" can never be ``False``,
        when ``background`` is omitted ``min_contrast`` defaults to ``7.0``
        (WCAG AAA) so mid-luminance colors with weak contrast on both light and
        dark surfaces are properly flagged. When a specific ``background`` is
        given, ``min_contrast`` defaults to ``4.5`` (WCAG AA).

    Parameters:
        rgb (tuple): RGB color ``(r, g, b)`` in ``[0, 255]``.
        background (tuple | None): Optional target background RGB color.
        min_contrast (float | None): Optional custom contrast threshold in ``[1, 21]``.

    Returns:
        dict: Contrast metrics and compliance flags including
        ``contrast_with_black``, ``contrast_with_white``, ``passes_aa_on_black``,
        ``passes_aa_on_white``, ``passes_aaa_on_black``, ``passes_aaa_on_white``,
        ``best_background``, ``is_good_quality``, and (when ``background`` is
        supplied) ``contrast_with_background``.
    """
    contrast_black = color_contrast(rgb, (0, 0, 0))
    contrast_white = color_contrast(rgb, (255, 255, 255))

    if min_contrast is not None:
        threshold = _validate_real(min_contrast, "min_contrast")
        if not 1.0 <= threshold <= 21.0:
            raise ValueError(f"min_contrast must be in the range [1, 21], got {min_contrast}.")
    else:
        threshold = 4.5 if background is not None else 7.0

    result: dict[str, Any] = {
        "contrast_with_black": round(contrast_black, 2),
        "contrast_with_white": round(contrast_white, 2),
        "passes_aa_on_black": contrast_black >= 4.5,
        "passes_aa_on_white": contrast_white >= 4.5,
        "passes_aaa_on_black": contrast_black >= 7.0,
        "passes_aaa_on_white": contrast_white >= 7.0,
        "best_background": "black" if contrast_black >= contrast_white else "white",
    }

    if background is not None:
        contrast_bg = color_contrast(rgb, background)
        result["contrast_with_background"] = round(contrast_bg, 2)
        result["is_good_quality"] = contrast_bg >= threshold
    else:
        result["is_good_quality"] = contrast_black >= threshold or contrast_white >= threshold

    return result


def simulate_color_blindness(
    rgb: Sequence[int],
    blindness_type: str = "protanopia",
    intensity: float = 1.0,
) -> tuple[int, int, int]:
    """Simulate color-vision deficiency on an RGB color.

    Performs the matrix transformation and severity interpolation in linear sRGB
    space and re-encodes using the exact IEC 61966-2-1 sRGB transfer function.

    Parameters:
        rgb (tuple): RGB color ``(r, g, b)`` in ``[0, 255]``.
        blindness_type (str): One of ``"protanopia"``, ``"deuteranopia"``,
            ``"tritanopia"``, or ``"achromatopsia"`` (case-insensitive).
        intensity (float): Simulation severity in ``[0.0, 1.0]`` (default ``1.0``).

    Returns:
        tuple[int, int, int]: Simulated RGB tuple in ``[0, 255]``.

    Raises:
        TypeError: If arguments have invalid types.
        ValueError: If ``blindness_type`` is unknown or ``intensity`` is outside ``[0, 1]``.
    """
    r_lin, g_lin, b_lin = rgb_to_linear(rgb)

    if not isinstance(blindness_type, str):
        raise TypeError(f"blindness_type must be a string, got {type(blindness_type).__name__}.")
    key = blindness_type.strip().lower()
    if key not in _CVD_MATRICES:
        supported = ", ".join(sorted(_CVD_MATRICES))
        raise ValueError(f"Unknown blindness type: {blindness_type!r}. Supported: {supported}.")

    t = _validate_real(intensity, "intensity")
    if not 0.0 <= t <= 1.0:
        raise ValueError("Intensity must be between 0 and 1.")

    matrix = _CVD_MATRICES[key]
    r_sim = r_lin * matrix[0][0] + g_lin * matrix[0][1] + b_lin * matrix[0][2]
    g_sim = r_lin * matrix[1][0] + g_lin * matrix[1][1] + b_lin * matrix[1][2]
    b_sim = r_lin * matrix[2][0] + g_lin * matrix[2][1] + b_lin * matrix[2][2]

    inv = 1.0 - t
    r_mix = r_lin * inv + r_sim * t
    g_mix = g_lin * inv + g_sim * t
    b_mix = b_lin * inv + b_sim * t

    return (
        max(0, min(255, round(_linear_to_srgb_channel(r_mix) * 255.0))),
        max(0, min(255, round(_linear_to_srgb_channel(g_mix) * 255.0))),
        max(0, min(255, round(_linear_to_srgb_channel(b_mix) * 255.0))),
    )


def _ciede2000(
    lab1: tuple[float, float, float],
    lab2: tuple[float, float, float],
) -> float:
    """Compute exact CIEDE2000 color difference (Sharma, Wu & Dalal 2005)."""
    l1, a1, b1 = lab1
    l2, a2, b2 = lab2

    c1 = math.hypot(a1, b1)
    c2 = math.hypot(a2, b2)
    c_bar = 0.5 * (c1 + c2)
    c_bar7 = c_bar**7
    pow25_7 = 6103515625.0  # 25 ** 7
    g = 0.5 * (1.0 - math.sqrt(c_bar7 / (c_bar7 + pow25_7)))

    a1p = (1.0 + g) * a1
    a2p = (1.0 + g) * a2
    c1p = math.hypot(a1p, b1)
    c2p = math.hypot(a2p, b2)

    h1p = 0.0 if (a1p == 0.0 and b1 == 0.0) else math.degrees(math.atan2(b1, a1p)) % 360.0
    h2p = 0.0 if (a2p == 0.0 and b2 == 0.0) else math.degrees(math.atan2(b2, a2p)) % 360.0

    dlp = l2 - l1
    dcp = c2p - c1p

    c_prod = c1p * c2p
    if c_prod == 0.0:
        dhp = 0.0
    else:
        diff = h2p - h1p
        if abs(diff) <= 180.0:
            dhp = diff
        elif diff > 180.0:
            dhp = diff - 360.0
        else:
            dhp = diff + 360.0

    dhp_term = 2.0 * math.sqrt(c_prod) * math.sin(math.radians(0.5 * dhp))

    lp_bar = 0.5 * (l1 + l2)
    cp_bar = 0.5 * (c1p + c2p)

    if c_prod == 0.0:
        hp_bar = h1p + h2p
    elif abs(h1p - h2p) <= 180.0:
        hp_bar = 0.5 * (h1p + h2p)
    elif h1p + h2p < 360.0:
        hp_bar = 0.5 * (h1p + h2p + 360.0)
    else:
        hp_bar = 0.5 * (h1p + h2p - 360.0)

    t_factor = (
        1.0
        - 0.17 * math.cos(math.radians(hp_bar - 30.0))
        + 0.24 * math.cos(math.radians(2.0 * hp_bar))
        + 0.32 * math.cos(math.radians(3.0 * hp_bar + 6.0))
        - 0.20 * math.cos(math.radians(4.0 * hp_bar - 63.0))
    )

    d_theta = 30.0 * math.exp(-(((hp_bar - 275.0) / 25.0) ** 2))
    cp_bar7 = cp_bar**7
    rc = 2.0 * math.sqrt(cp_bar7 / (cp_bar7 + pow25_7))
    lp_minus_50_sq = (lp_bar - 50.0) ** 2
    sl = 1.0 + (0.015 * lp_minus_50_sq) / math.sqrt(20.0 + lp_minus_50_sq)
    sc = 1.0 + 0.045 * cp_bar
    sh = 1.0 + 0.015 * cp_bar * t_factor
    rt = -math.sin(math.radians(2.0 * d_theta)) * rc

    l_term = dlp / sl
    c_term = dcp / sc
    h_term = dhp_term / sh
    sq = l_term * l_term + c_term * c_term + h_term * h_term + rt * c_term * h_term
    return math.sqrt(max(0.0, sq))


def delta_e(
    color1: Sequence[int],
    color2: Sequence[int],
    method: str = "cie2000",
) -> float:
    """Calculate the perceptual color difference (Delta E) between two RGB colors.

    A Delta E below ~``1.0`` is typically imperceptible to the human eye;
    ``1–2`` is noticeable only on close inspection; ``2–10`` is perceptible at a
    glance; ``100`` represents completely opposite colors.

    Parameters:
        color1 (tuple): First RGB color ``(r, g, b)`` in ``[0, 255]``.
        color2 (tuple): Second RGB color ``(r, g, b)`` in ``[0, 255]``.
        method (str): ``"cie2000"`` (default, CIEDE2000 standard) or ``"cie76"``
            (Euclidean distance in CIE 1976 L*a*b*).

    Returns:
        float: Non-negative Delta E perceptual color difference.
    """
    r1, g1, b1 = _validate_rgb_number_tuple(color1, "color1")
    r2, g2, b2 = _validate_rgb_number_tuple(color2, "color2")
    if not isinstance(method, str):
        raise TypeError(f"method must be a string, got {type(method).__name__}.")

    lab1 = rgb_to_lab(r1, g1, b1)  # type: ignore[arg-type]
    lab2 = rgb_to_lab(r2, g2, b2)  # type: ignore[arg-type]

    mode = method.strip().lower()
    if mode == "cie2000":
        return _ciede2000(lab1, lab2)
    if mode == "cie76":
        return math.sqrt(
            (lab2[0] - lab1[0]) ** 2
            + (lab2[1] - lab1[1]) ** 2
            + (lab2[2] - lab1[2]) ** 2
        )
    raise ValueError(f"Unknown Delta E method: {method!r}. Use 'cie2000' or 'cie76'.")
