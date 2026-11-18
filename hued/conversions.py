"""Color space conversion and color manipulation utilities."""

from __future__ import annotations

import math
import re
from collections.abc import Sequence

__all__ = [
    "rgb_to_hex",
    "hex_to_rgb",
    "rgb_to_hsl",
    "hsl_to_rgb",
    "rgb_to_hsv",
    "hsv_to_rgb",
    "rgb_to_cmyk",
    "cmyk_to_rgb",
    "hex_to_hsl",
    "hex_to_hsv",
    "hex_to_cmyk",
    "hsl_to_hex",
    "hsl_to_hsv",
    "hsl_to_cmyk",
    "hsv_to_hex",
    "hsv_to_hsl",
    "hsv_to_cmyk",
    "cmyk_to_hex",
    "cmyk_to_hsv",
    "cmyk_to_hsl",
    "rgb_to_xyz",
    "xyz_to_rgb",
    "hex_to_xyz",
    "xyz_to_hex",
    "hsl_to_xyz",
    "xyz_to_hsl",
    "hsv_to_xyz",
    "xyz_to_hsv",
    "cmyk_to_xyz",
    "xyz_to_cmyk",
    "rgb_to_lab",
    "lab_to_rgb",
    "xyz_to_lab",
    "lab_to_xyz",
    "hex_to_lab",
    "lab_to_hex",
    "hsl_to_lab",
    "lab_to_hsl",
    "hsv_to_lab",
    "lab_to_hsv",
    "cmyk_to_lab",
    "lab_to_cmyk",
    "linear_to_rgb",
    "blend_colors",
    "invert_color",
    "to_grayscale",
    "adjust_lightness",
    "adjust_saturation",
]

_HEX_DIGITS_RE = re.compile(r"^[0-9A-Fa-f]+$")

# Standard CIE D65 2-degree reference white matching the IEC 61966-2-1 sRGB matrix.
_D65_X = 0.95047
_D65_Y = 1.00000
_D65_Z = 1.08883

# Exact CIE L*a*b* transfer constants.
_LAB_EPSILON = 216.0 / 24389.0  # (6/29)^3 ~= 0.008856
_LAB_KAPPA = 24389.0 / 27.0  # (29/3)^3 ~= 903.296296
_LAB_DELTA = 6.0 / 29.0


def _validate_real(value: float, name: str) -> float:
    """Validate that ``value`` is a finite real number (rejecting ``bool``)."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real number, got {type(value).__name__}.")
    if not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number, got {value!r}.")
    return float(value)


def _validate_int_channel(value: int, name: str) -> int:
    """Validate an integer RGB channel in ``[0, 255]`` (rejecting ``bool``)."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer in [0, 255], got {type(value).__name__}.")
    if not 0 <= value <= 255:
        raise ValueError(f"{name} must be in the range [0, 255], got {value}.")
    return value


def _validate_rgb_channels(r: float, g: float, b: float) -> tuple[float, float, float]:
    """Validate three RGB components in ``[0, 255]``."""
    rf = _validate_real(r, "r")
    gf = _validate_real(g, "g")
    bf = _validate_real(b, "b")
    if not (0.0 <= rf <= 255.0 and 0.0 <= gf <= 255.0 and 0.0 <= bf <= 255.0):
        raise ValueError("RGB values must be in the range [0, 255].")
    return rf, gf, bf


def _validate_sequence(value: Sequence[float], length: int, name: str) -> tuple[float, ...]:
    """Unpack and validate a fixed-length numeric tuple/list."""
    if not isinstance(value, (tuple, list)):
        raise TypeError(f"{name} must be a tuple or list of {length} numbers, got {type(value).__name__}.")
    if len(value) != length:
        raise ValueError(f"{name} must have exactly {length} elements, got {len(value)}.")
    return tuple(value)


def _validate_rgb_tuple(rgb: Sequence[int], name: str = "rgb") -> tuple[int, int, int]:
    """Validate a 3-element integer RGB sequence in ``[0, 255]``."""
    r, g, b = _validate_sequence(rgb, 3, name)
    return (
        _validate_int_channel(r, f"{name}[0]"),  # type: ignore[arg-type]
        _validate_int_channel(g, f"{name}[1]"),  # type: ignore[arg-type]
        _validate_int_channel(b, f"{name}[2]"),  # type: ignore[arg-type]
    )


def _validate_rgb_number_tuple(rgb: Sequence[float], name: str = "rgb") -> tuple[float, float, float]:
    """Validate a 3-element real RGB sequence in ``[0, 255]``."""
    r, g, b = _validate_sequence(rgb, 3, name)
    return _validate_rgb_channels(r, g, b)


def _validate_hsl(h: float, s: float, l: float) -> tuple[float, float, float]:
    hf = _validate_real(h, "h")
    sf = _validate_real(s, "s")
    lf = _validate_real(l, "l")
    if not (0.0 <= hf < 360.0 and 0.0 <= sf <= 1.0 and 0.0 <= lf <= 1.0):
        raise ValueError("HSL values must be in range: h [0, 360), s [0, 1], l [0, 1].")
    return hf, sf, lf


def _validate_hsv(h: float, s: float, v: float) -> tuple[float, float, float]:
    hf = _validate_real(h, "h")
    sf = _validate_real(s, "s")
    vf = _validate_real(v, "v")
    if not (0.0 <= hf < 360.0 and 0.0 <= sf <= 1.0 and 0.0 <= vf <= 1.0):
        raise ValueError("HSV values must be in range: h [0, 360), s [0, 1], v [0, 1].")
    return hf, sf, vf


def _validate_cmyk(c: float, m: float, y: float, k: float) -> tuple[float, float, float, float]:
    cf = _validate_real(c, "c")
    mf = _validate_real(m, "m")
    yf = _validate_real(y, "y")
    kf = _validate_real(k, "k")
    if not (0.0 <= cf <= 1.0 and 0.0 <= mf <= 1.0 and 0.0 <= yf <= 1.0 and 0.0 <= kf <= 1.0):
        raise ValueError("CMYK values must be in range: c, m, y, k [0, 1].")
    return cf, mf, yf, kf


def _validate_xyz(x: float, y: float, z: float) -> tuple[float, float, float]:
    xf = _validate_real(x, "x")
    yf = _validate_real(y, "y")
    zf = _validate_real(z, "z")
    if xf < 0.0 or yf < 0.0 or zf < 0.0:
        raise ValueError("XYZ values must be non-negative.")
    return xf, yf, zf


def _validate_lab(l: float, a: float, b: float) -> tuple[float, float, float]:
    lf = _validate_real(l, "l")
    af = _validate_real(a, "a")
    bf = _validate_real(b, "b")
    if not 0.0 <= lf <= 100.0:
        raise ValueError("LAB lightness L* must be in the range [0, 100].")
    return lf, af, bf


def _srgb_to_linear_channel(channel: float) -> float:
    """Apply the IEC 61966-2-1 sRGB inverse companding function to a ``[0, 255]`` channel."""
    s = channel / 255.0
    if s <= 0.04045:
        return s / 12.92
    return ((s + 0.055) / 1.055) ** 2.4


def _linear_to_srgb_channel(linear: float) -> float:
    """Apply the IEC 61966-2-1 sRGB companding function to a linear value, clamped to ``[0, 1]``."""
    c = max(0.0, min(1.0, linear))
    if c <= 0.0031308:
        return 12.92 * c
    return 1.055 * (c ** (1.0 / 2.4)) - 0.055


def _wrap_hue(angle: float) -> float:
    """Wrap an angle in degrees strictly into ``[0.0, 360.0)`` (handling ``-1e-15 % 360 == 360``)."""
    wrapped = angle % 360.0
    if wrapped >= 360.0 or wrapped == 0.0:
        return 0.0
    return wrapped


def _rgb_to_hsl_exact(r: float, g: float, b: float) -> tuple[float, float, float]:
    """Full-precision RGB ``[0, 255]`` to HSL conversion without rounding."""
    rn, gn, bn = r / 255.0, g / 255.0, b / 255.0
    max_c = max(rn, gn, bn)
    min_c = min(rn, gn, bn)
    delta = max_c - min_c
    l = (max_c + min_c) / 2.0

    if delta == 0.0:
        return 0.0, 0.0, l

    s = delta / (1.0 - abs(2.0 * l - 1.0))
    if max_c == rn:
        h = ((gn - bn) / delta) % 6.0
    elif max_c == gn:
        h = (bn - rn) / delta + 2.0
    else:
        h = (rn - gn) / delta + 4.0
    return _wrap_hue(h * 60.0), min(1.0, max(0.0, s)), min(1.0, max(0.0, l))


def _rgb_to_hsv_exact(r: float, g: float, b: float) -> tuple[float, float, float]:
    """Full-precision RGB ``[0, 255]`` to HSV conversion without rounding."""
    rn, gn, bn = r / 255.0, g / 255.0, b / 255.0
    max_c = max(rn, gn, bn)
    min_c = min(rn, gn, bn)
    delta = max_c - min_c
    v = max_c

    if delta == 0.0:
        return 0.0, 0.0, v

    s = delta / max_c
    if max_c == rn:
        h = ((gn - bn) / delta) % 6.0
    elif max_c == gn:
        h = (bn - rn) / delta + 2.0
    else:
        h = (rn - gn) / delta + 4.0
    return _wrap_hue(h * 60.0), min(1.0, max(0.0, s)), min(1.0, max(0.0, v))


def _round_hue(h: float) -> float:
    """Round hue to 2 decimal places while strictly preserving ``[0, 360)``."""
    rounded = round(h, 2)
    if rounded >= 360.0 or rounded == 0.0:
        return 0.0
    return rounded


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Convert integer RGB values to an uppercase 6-digit hex color code.

    Parameters:
        r (int): Red component in ``[0, 255]``.
        g (int): Green component in ``[0, 255]``.
        b (int): Blue component in ``[0, 255]``.

    Returns:
        str: Uppercase hex color string (e.g., ``"#FF0000"``).

    Raises:
        TypeError: If any component is not an integer.
        ValueError: If any component is outside ``[0, 255]``.
    """
    ri = _validate_int_channel(r, "r")
    gi = _validate_int_channel(g, "g")
    bi = _validate_int_channel(b, "b")
    return f"#{ri:02X}{gi:02X}{bi:02X}"


def hex_to_rgb(hex_value: str) -> tuple[int, int, int]:
    """Convert a 3- or 6-digit hex color code to an RGB tuple.

    Supports leading ``#`` (optional), 3-digit shorthand (e.g., ``"#F0A"``),
    case-insensitive hex digits, and surrounding whitespace.

    Parameters:
        hex_value (str): Hex color code (e.g., ``"#FFFFFF"``, ``"FF5733"``, ``"#FFF"``).

    Returns:
        tuple[int, int, int]: RGB values in ``[0, 255]``.

    Raises:
        TypeError: If ``hex_value`` is not a string.
        ValueError: If ``hex_value`` is not a valid 3- or 6-digit hex color code.
    """
    if not isinstance(hex_value, str):
        raise TypeError(f"hex_value must be a string, got {type(hex_value).__name__}.")

    cleaned = hex_value.strip()
    if cleaned.startswith("#"):
        cleaned = cleaned[1:]

    if len(cleaned) == 3:
        cleaned = "".join(ch * 2 for ch in cleaned)
    elif len(cleaned) != 6:
        raise ValueError(
            f"Invalid hex color {hex_value!r}: expected 3 or 6 hexadecimal digits."
        )

    if not _HEX_DIGITS_RE.match(cleaned):
        raise ValueError(
            f"Invalid hex color {hex_value!r}: contains non-hexadecimal characters."
        )

    return (
        int(cleaned[0:2], 16),
        int(cleaned[2:4], 16),
        int(cleaned[4:6], 16),
    )


def rgb_to_hsl(r: int, g: int, b: int) -> tuple[float, float, float]:
    """Convert RGB values to HSL (Hue, Saturation, Lightness).

    Parameters:
        r (int): Red value in ``[0, 255]``.
        g (int): Green value in ``[0, 255]``.
        b (int): Blue value in ``[0, 255]``.

    Returns:
        tuple[float, float, float]: ``(h, s, l)`` with ``h`` in ``[0, 360)``
        and ``s``, ``l`` in ``[0, 1]``, rounded to 2 decimal places.
    """
    rf, gf, bf = _validate_rgb_channels(r, g, b)
    h, s, l = _rgb_to_hsl_exact(rf, gf, bf)
    return _round_hue(h), round(s, 2), round(l, 2)


def hsl_to_rgb(h: float, s: float, l: float) -> tuple[int, int, int]:
    """Convert HSL (Hue, Saturation, Lightness) values to RGB.

    Parameters:
        h (float): Hue in ``[0, 360)``.
        s (float): Saturation in ``[0, 1]``.
        l (float): Lightness in ``[0, 1]``.

    Returns:
        tuple[int, int, int]: RGB values in ``[0, 255]``.

    Raises:
        TypeError: If any argument is not a real number.
        ValueError: If any HSL component is outside its valid range.
    """
    hf, sf, lf = _validate_hsl(h, s, l)
    c = (1.0 - abs(2.0 * lf - 1.0)) * sf
    x = c * (1.0 - abs((hf / 60.0) % 2.0 - 1.0))
    m = lf - c / 2.0

    if hf < 60.0:
        r, g, b = c, x, 0.0
    elif hf < 120.0:
        r, g, b = x, c, 0.0
    elif hf < 180.0:
        r, g, b = 0.0, c, x
    elif hf < 240.0:
        r, g, b = 0.0, x, c
    elif hf < 300.0:
        r, g, b = x, 0.0, c
    else:
        r, g, b = c, 0.0, x

    return (
        max(0, min(255, round((r + m) * 255.0))),
        max(0, min(255, round((g + m) * 255.0))),
        max(0, min(255, round((b + m) * 255.0))),
    )


def rgb_to_hsv(r: int, g: int, b: int) -> tuple[float, float, float]:
    """Convert RGB values to HSV (Hue, Saturation, Value).

    Parameters:
        r (int): Red value in ``[0, 255]``.
        g (int): Green value in ``[0, 255]``.
        b (int): Blue value in ``[0, 255]``.

    Returns:
        tuple[float, float, float]: ``(h, s, v)`` with ``h`` in ``[0, 360)``
        and ``s``, ``v`` in ``[0, 1]``, rounded to 2 decimal places.
    """
    rf, gf, bf = _validate_rgb_channels(r, g, b)
    h, s, v = _rgb_to_hsv_exact(rf, gf, bf)
    return _round_hue(h), round(s, 2), round(v, 2)


def hsv_to_rgb(h: float, s: float, v: float) -> tuple[int, int, int]:
    """Convert HSV (Hue, Saturation, Value) values to RGB.

    Parameters:
        h (float): Hue in ``[0, 360)``.
        s (float): Saturation in ``[0, 1]``.
        v (float): Value in ``[0, 1]``.

    Returns:
        tuple[int, int, int]: RGB values in ``[0, 255]``.

    Raises:
        TypeError: If any argument is not a real number.
        ValueError: If any HSV component is outside its valid range.
    """
    hf, sf, vf = _validate_hsv(h, s, v)
    c = vf * sf
    x = c * (1.0 - abs((hf / 60.0) % 2.0 - 1.0))
    m = vf - c

    if hf < 60.0:
        r, g, b = c, x, 0.0
    elif hf < 120.0:
        r, g, b = x, c, 0.0
    elif hf < 180.0:
        r, g, b = 0.0, c, x
    elif hf < 240.0:
        r, g, b = 0.0, x, c
    elif hf < 300.0:
        r, g, b = x, 0.0, c
    else:
        r, g, b = c, 0.0, x

    return (
        max(0, min(255, round((r + m) * 255.0))),
        max(0, min(255, round((g + m) * 255.0))),
        max(0, min(255, round((b + m) * 255.0))),
    )


def rgb_to_cmyk(r: int, g: int, b: int) -> tuple[float, float, float, float]:
    """Convert RGB values to CMYK (Cyan, Magenta, Yellow, Key/Black).

    Parameters:
        r (int): Red value in ``[0, 255]``.
        g (int): Green value in ``[0, 255]``.
        b (int): Blue value in ``[0, 255]``.

    Returns:
        tuple[float, float, float, float]: ``(c, m, y, k)`` each in ``[0, 1]``,
        rounded to 2 decimal places.
    """
    rf, gf, bf = _validate_rgb_channels(r, g, b)
    if rf == 0.0 and gf == 0.0 and bf == 0.0:
        return 0.0, 0.0, 0.0, 1.0

    c = 1.0 - rf / 255.0
    m = 1.0 - gf / 255.0
    y = 1.0 - bf / 255.0
    k = min(c, m, y)

    denom = 1.0 - k
    c = (c - k) / denom
    m = (m - k) / denom
    y = (y - k) / denom

    return round(c, 2), round(m, 2), round(y, 2), round(k, 2)


def cmyk_to_rgb(c: float, m: float, y: float, k: float) -> tuple[int, int, int]:
    """Convert CMYK values to RGB.

    Parameters:
        c (float): Cyan in ``[0, 1]``.
        m (float): Magenta in ``[0, 1]``.
        y (float): Yellow in ``[0, 1]``.
        k (float): Key/black in ``[0, 1]``.

    Returns:
        tuple[int, int, int]: RGB values in ``[0, 255]``.

    Raises:
        TypeError: If any argument is not a real number.
        ValueError: If any CMYK component is outside ``[0, 1]``.
    """
    cf, mf, yf, kf = _validate_cmyk(c, m, y, k)
    r = 255.0 * (1.0 - cf) * (1.0 - kf)
    g = 255.0 * (1.0 - mf) * (1.0 - kf)
    b = 255.0 * (1.0 - yf) * (1.0 - kf)
    return round(r), round(g), round(b)


def hex_to_hsl(hex_value: str) -> tuple[float, float, float]:
    """Convert a hex color code to HSL."""
    return rgb_to_hsl(*hex_to_rgb(hex_value))


def hex_to_hsv(hex_value: str) -> tuple[float, float, float]:
    """Convert a hex color code to HSV."""
    return rgb_to_hsv(*hex_to_rgb(hex_value))


def hex_to_cmyk(hex_value: str) -> tuple[float, float, float, float]:
    """Convert a hex color code to CMYK."""
    return rgb_to_cmyk(*hex_to_rgb(hex_value))


def hsl_to_hex(hsl_value: Sequence[float]) -> str:
    """Convert an HSL tuple ``(h, s, l)`` to a hex color code."""
    h, s, l = _validate_hsl(*_validate_sequence(hsl_value, 3, "hsl_value"))
    return rgb_to_hex(*hsl_to_rgb(h, s, l))


def hsl_to_hsv(hsl_value: Sequence[float]) -> tuple[float, float, float]:
    """Convert an HSL tuple ``(h, s, l)`` directly to HSV without 8-bit RGB loss."""
    h, s, l = _validate_hsl(*_validate_sequence(hsl_value, 3, "hsl_value"))
    v = l + s * min(l, 1.0 - l)
    sv = 0.0 if v == 0.0 else 2.0 * (1.0 - l / v)
    hv = 0.0 if sv == 0.0 else h
    return _round_hue(hv), round(sv, 2), round(v, 2)


def hsl_to_cmyk(hsl_value: Sequence[float]) -> tuple[float, float, float, float]:
    """Convert an HSL tuple ``(h, s, l)`` to CMYK."""
    h, s, l = _validate_hsl(*_validate_sequence(hsl_value, 3, "hsl_value"))
    return rgb_to_cmyk(*hsl_to_rgb(h, s, l))


def hsv_to_hex(hsv_value: Sequence[float]) -> str:
    """Convert an HSV tuple ``(h, s, v)`` to a hex color code."""
    h, s, v = _validate_hsv(*_validate_sequence(hsv_value, 3, "hsv_value"))
    return rgb_to_hex(*hsv_to_rgb(h, s, v))


def hsv_to_hsl(hsv_value: Sequence[float]) -> tuple[float, float, float]:
    """Convert an HSV tuple ``(h, s, v)`` directly to HSL without 8-bit RGB loss."""
    h, s, v = _validate_hsv(*_validate_sequence(hsv_value, 3, "hsv_value"))
    l = v * (1.0 - s / 2.0)
    sl = 0.0 if (l == 0.0 or l == 1.0) else (v - l) / min(l, 1.0 - l)
    hl = 0.0 if sl == 0.0 else h
    return _round_hue(hl), round(sl, 2), round(l, 2)


def hsv_to_cmyk(hsv_value: Sequence[float]) -> tuple[float, float, float, float]:
    """Convert an HSV tuple ``(h, s, v)`` to CMYK."""
    h, s, v = _validate_hsv(*_validate_sequence(hsv_value, 3, "hsv_value"))
    return rgb_to_cmyk(*hsv_to_rgb(h, s, v))


def cmyk_to_hex(cmyk_value: Sequence[float]) -> str:
    """Convert a CMYK tuple ``(c, m, y, k)`` to a hex color code."""
    c, m, y, k = _validate_cmyk(*_validate_sequence(cmyk_value, 4, "cmyk_value"))
    return rgb_to_hex(*cmyk_to_rgb(c, m, y, k))


def cmyk_to_hsv(cmyk_value: Sequence[float]) -> tuple[float, float, float]:
    """Convert a CMYK tuple ``(c, m, y, k)`` to HSV."""
    c, m, y, k = _validate_cmyk(*_validate_sequence(cmyk_value, 4, "cmyk_value"))
    return rgb_to_hsv(*cmyk_to_rgb(c, m, y, k))


def cmyk_to_hsl(cmyk_value: Sequence[float]) -> tuple[float, float, float]:
    """Convert a CMYK tuple ``(c, m, y, k)`` to HSL."""
    c, m, y, k = _validate_cmyk(*_validate_sequence(cmyk_value, 4, "cmyk_value"))
    return rgb_to_hsl(*cmyk_to_rgb(c, m, y, k))


def rgb_to_xyz(r: int, g: int, b: int) -> tuple[float, float, float]:
    """Convert sRGB ``(r, g, b)`` to CIE 1931 XYZ (D65 standard illuminant).

    Uses the standard IEC 61966-2-1 sRGB transfer function and D65 matrix,
    returning values normalized so D65 white has ``Y = 1.0``.

    Parameters:
        r (int): Red component in ``[0, 255]``.
        g (int): Green component in ``[0, 255]``.
        b (int): Blue component in ``[0, 255]``.

    Returns:
        tuple[float, float, float]: ``(x, y, z)`` in CIE 1931 XYZ space.
    """
    rf, gf, bf = _validate_rgb_channels(r, g, b)
    r_lin = _srgb_to_linear_channel(rf)
    g_lin = _srgb_to_linear_channel(gf)
    b_lin = _srgb_to_linear_channel(bf)

    x = 0.4124564 * r_lin + 0.3575761 * g_lin + 0.1804375 * b_lin
    y = 0.2126729 * r_lin + 0.7151522 * g_lin + 0.0721749 * b_lin
    z = 0.0193339 * r_lin + 0.1191920 * g_lin + 0.9503041 * b_lin

    return x, y, z


def xyz_to_rgb(x: float, y: float, z: float) -> tuple[int, int, int]:
    """Convert CIE 1931 XYZ (D65) to sRGB ``(r, g, b)``.

    Uses the standard IEC 61966-2-1 inverse matrix and sRGB companding
    function. Out-of-sRGB-gamut values are safely clamped to ``[0, 255]``.

    Parameters:
        x (float): X component (``>= 0``).
        y (float): Y component (``>= 0``).
        z (float): Z component (``>= 0``).

    Returns:
        tuple[int, int, int]: RGB values in ``[0, 255]``.
    """
    xf, yf, zf = _validate_xyz(x, y, z)

    r_lin = 3.2404542 * xf - 1.5371385 * yf - 0.4985314 * zf
    g_lin = -0.9692660 * xf + 1.8760108 * yf + 0.0415560 * zf
    b_lin = 0.0556434 * xf - 0.2040259 * yf + 1.0572252 * zf

    r = round(_linear_to_srgb_channel(r_lin) * 255.0)
    g = round(_linear_to_srgb_channel(g_lin) * 255.0)
    b = round(_linear_to_srgb_channel(b_lin) * 255.0)

    return max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b))


def hex_to_xyz(hex_value: str) -> tuple[float, float, float]:
    """Convert a hex color code to CIE 1931 XYZ (D65)."""
    return rgb_to_xyz(*hex_to_rgb(hex_value))


def xyz_to_hex(xyz_value: Sequence[float]) -> str:
    """Convert a CIE 1931 XYZ tuple ``(x, y, z)`` to a hex color code."""
    x, y, z = _validate_xyz(*_validate_sequence(xyz_value, 3, "xyz_value"))
    return rgb_to_hex(*xyz_to_rgb(x, y, z))


def hsl_to_xyz(hsl_value: Sequence[float]) -> tuple[float, float, float]:
    """Convert an HSL tuple ``(h, s, l)`` to CIE 1931 XYZ (D65)."""
    h, s, l = _validate_hsl(*_validate_sequence(hsl_value, 3, "hsl_value"))
    return rgb_to_xyz(*hsl_to_rgb(h, s, l))


def xyz_to_hsl(xyz_value: Sequence[float]) -> tuple[float, float, float]:
    """Convert a CIE 1931 XYZ tuple ``(x, y, z)`` to HSL."""
    x, y, z = _validate_xyz(*_validate_sequence(xyz_value, 3, "xyz_value"))
    return rgb_to_hsl(*xyz_to_rgb(x, y, z))


def hsv_to_xyz(hsv_value: Sequence[float]) -> tuple[float, float, float]:
    """Convert an HSV tuple ``(h, s, v)`` to CIE 1931 XYZ (D65)."""
    h, s, v = _validate_hsv(*_validate_sequence(hsv_value, 3, "hsv_value"))
    return rgb_to_xyz(*hsv_to_rgb(h, s, v))


def xyz_to_hsv(xyz_value: Sequence[float]) -> tuple[float, float, float]:
    """Convert a CIE 1931 XYZ tuple ``(x, y, z)`` to HSV."""
    x, y, z = _validate_xyz(*_validate_sequence(xyz_value, 3, "xyz_value"))
    return rgb_to_hsv(*xyz_to_rgb(x, y, z))


def xyz_to_cmyk(xyz_value: Sequence[float]) -> tuple[float, float, float, float]:
    """Convert a CIE 1931 XYZ tuple ``(x, y, z)`` to CMYK."""
    x, y, z = _validate_xyz(*_validate_sequence(xyz_value, 3, "xyz_value"))
    return rgb_to_cmyk(*xyz_to_rgb(x, y, z))


def cmyk_to_xyz(cmyk_value: Sequence[float]) -> tuple[float, float, float]:
    """Convert a CMYK tuple ``(c, m, y, k)`` to CIE 1931 XYZ (D65)."""
    c, m, y, k = _validate_cmyk(*_validate_sequence(cmyk_value, 4, "cmyk_value"))
    return rgb_to_xyz(*cmyk_to_rgb(c, m, y, k))


def xyz_to_lab(xyz_value: Sequence[float]) -> tuple[float, float, float]:
    """Convert a CIE 1931 XYZ (D65) tuple ``(x, y, z)`` to CIE 1976 L*a*b*.

    Parameters:
        xyz_value (tuple): ``(x, y, z)`` coordinates under illuminant D65.

    Returns:
        tuple[float, float, float]: ``(L*, a*, b*)`` where ``L*`` is in
        ``[0, 100]`` and ``a*``, ``b*`` represent green-red and blue-yellow axes.
    """
    x, y, z = _validate_xyz(*_validate_sequence(xyz_value, 3, "xyz_value"))

    def _f(t: float) -> float:
        if t > _LAB_EPSILON:
            return t ** (1.0 / 3.0)
        return (_LAB_KAPPA * t + 16.0) / 116.0

    fx = _f(x / _D65_X)
    fy = _f(y / _D65_Y)
    fz = _f(z / _D65_Z)

    l_star = max(0.0, 116.0 * fy - 16.0)
    if 100.0 < l_star <= 100.0001:
        l_star = 100.0
    a_star = 500.0 * (fx - fy)
    b_star = 200.0 * (fy - fz)
    return l_star, a_star, b_star


def lab_to_xyz(lab_value: Sequence[float]) -> tuple[float, float, float]:
    """Convert a CIE 1976 L*a*b* tuple ``(L*, a*, b*)`` to CIE 1931 XYZ (D65).

    Parameters:
        lab_value (tuple): ``(L*, a*, b*)`` coordinates with ``L*`` in ``[0, 100]``.

    Returns:
        tuple[float, float, float]: ``(x, y, z)`` under illuminant D65.
    """
    l_star, a_star, b_star = _validate_lab(*_validate_sequence(lab_value, 3, "lab_value"))

    fy = (l_star + 16.0) / 116.0
    fx = a_star / 500.0 + fy
    fz = fy - b_star / 200.0

    xr = fx**3 if fx > _LAB_DELTA else (116.0 * fx - 16.0) / _LAB_KAPPA
    yr = ((l_star + 16.0) / 116.0) ** 3 if l_star > _LAB_KAPPA * _LAB_EPSILON else l_star / _LAB_KAPPA
    zr = fz**3 if fz > _LAB_DELTA else (116.0 * fz - 16.0) / _LAB_KAPPA

    return max(0.0, xr * _D65_X), max(0.0, yr * _D65_Y), max(0.0, zr * _D65_Z)


def rgb_to_lab(r: int, g: int, b: int) -> tuple[float, float, float]:
    """Convert sRGB ``(r, g, b)`` to CIE 1976 L*a*b* (D65).

    Parameters:
        r (int): Red component in ``[0, 255]``.
        g (int): Green component in ``[0, 255]``.
        b (int): Blue component in ``[0, 255]``.

    Returns:
        tuple[float, float, float]: ``(L*, a*, b*)`` coordinates.
    """
    return xyz_to_lab(rgb_to_xyz(r, g, b))


def lab_to_rgb(l: float, a: float, b: float) -> tuple[int, int, int]:
    """Convert CIE 1976 L*a*b* (D65) to sRGB ``(r, g, b)``.

    Out-of-sRGB-gamut values are safely clamped to ``[0, 255]``.

    Parameters:
        l (float): Lightness ``L*`` in ``[0, 100]``.
        a (float): Green-red opponent component ``a*``.
        b (float): Blue-yellow opponent component ``b*``.

    Returns:
        tuple[int, int, int]: RGB values in ``[0, 255]``.
    """
    return xyz_to_rgb(*lab_to_xyz((l, a, b)))


def hex_to_lab(hex_value: str) -> tuple[float, float, float]:
    """Convert a hex color code to CIE 1976 L*a*b* (D65)."""
    return rgb_to_lab(*hex_to_rgb(hex_value))


def lab_to_hex(lab_value: Sequence[float]) -> str:
    """Convert a CIE 1976 L*a*b* tuple ``(L*, a*, b*)`` to a hex color code."""
    l_star, a_star, b_star = _validate_lab(*_validate_sequence(lab_value, 3, "lab_value"))
    return rgb_to_hex(*lab_to_rgb(l_star, a_star, b_star))


def hsl_to_lab(hsl_value: Sequence[float]) -> tuple[float, float, float]:
    """Convert an HSL tuple ``(h, s, l)`` to CIE 1976 L*a*b* (D65)."""
    h, s, l = _validate_hsl(*_validate_sequence(hsl_value, 3, "hsl_value"))
    return rgb_to_lab(*hsl_to_rgb(h, s, l))


def lab_to_hsl(lab_value: Sequence[float]) -> tuple[float, float, float]:
    """Convert a CIE 1976 L*a*b* tuple ``(L*, a*, b*)`` to HSL."""
    l_star, a_star, b_star = _validate_lab(*_validate_sequence(lab_value, 3, "lab_value"))
    return rgb_to_hsl(*lab_to_rgb(l_star, a_star, b_star))


def hsv_to_lab(hsv_value: Sequence[float]) -> tuple[float, float, float]:
    """Convert an HSV tuple ``(h, s, v)`` to CIE 1976 L*a*b* (D65)."""
    h, s, v = _validate_hsv(*_validate_sequence(hsv_value, 3, "hsv_value"))
    return rgb_to_lab(*hsv_to_rgb(h, s, v))


def lab_to_hsv(lab_value: Sequence[float]) -> tuple[float, float, float]:
    """Convert a CIE 1976 L*a*b* tuple ``(L*, a*, b*)`` to HSV."""
    l_star, a_star, b_star = _validate_lab(*_validate_sequence(lab_value, 3, "lab_value"))
    return rgb_to_hsv(*lab_to_rgb(l_star, a_star, b_star))


def cmyk_to_lab(cmyk_value: Sequence[float]) -> tuple[float, float, float]:
    """Convert a CMYK tuple ``(c, m, y, k)`` to CIE 1976 L*a*b* (D65)."""
    c, m, y, k = _validate_cmyk(*_validate_sequence(cmyk_value, 4, "cmyk_value"))
    return rgb_to_lab(*cmyk_to_rgb(c, m, y, k))


def lab_to_cmyk(lab_value: Sequence[float]) -> tuple[float, float, float, float]:
    """Convert a CIE 1976 L*a*b* tuple ``(L*, a*, b*)`` to CMYK."""
    l_star, a_star, b_star = _validate_lab(*_validate_sequence(lab_value, 3, "lab_value"))
    return rgb_to_cmyk(*lab_to_rgb(l_star, a_star, b_star))


def linear_to_rgb(linear_rgb: Sequence[float]) -> tuple[int, int, int]:
    """Convert linear sRGB components in ``[0, 1]`` to 8-bit sRGB ``(r, g, b)``.

    Applies the IEC 61966-2-1 sRGB companding function (the exact inverse of
    :func:`hued.analysis.rgb_to_linear`).

    Parameters:
        linear_rgb (Sequence[float]): Three linear components in ``[0, 1]``.

    Returns:
        tuple[int, int, int]: sRGB values in ``[0, 255]``.
    """
    r, g, b = _validate_sequence(linear_rgb, 3, "linear_rgb")
    rf = _validate_real(r, "linear_rgb[0]")
    gf = _validate_real(g, "linear_rgb[1]")
    bf = _validate_real(b, "linear_rgb[2]")
    if not (0.0 <= rf <= 1.0 and 0.0 <= gf <= 1.0 and 0.0 <= bf <= 1.0):
        raise ValueError("Linear RGB values must be in the range [0, 1].")
    return (
        max(0, min(255, round(_linear_to_srgb_channel(rf) * 255.0))),
        max(0, min(255, round(_linear_to_srgb_channel(gf) * 255.0))),
        max(0, min(255, round(_linear_to_srgb_channel(bf) * 255.0))),
    )


def blend_colors(
    color1: Sequence[int],
    color2: Sequence[int],
    ratio: float = 0.5,
    *,
    linear: bool = False,
) -> tuple[int, int, int]:
    """Blend two RGB colors according to ``ratio``.

    Parameters:
        color1 (tuple): First RGB color ``(r, g, b)`` in ``[0, 255]``.
        color2 (tuple): Second RGB color ``(r, g, b)`` in ``[0, 255]``.
        ratio (float): Interpolation factor in ``[0, 1]`` (``0.0`` returns
            ``color1``, ``1.0`` returns ``color2``, ``0.5`` is an equal mix).
        linear (bool): If ``True``, perform physically accurate blending in
            linear sRGB light space instead of gamma-encoded sRGB.

    Returns:
        tuple[int, int, int]: Blended RGB color in ``[0, 255]``.

    Raises:
        TypeError: If colors or ``ratio`` have invalid types.
        ValueError: If RGB components are outside ``[0, 255]`` or ``ratio`` is outside ``[0, 1]``.
    """
    r1, g1, b1 = _validate_rgb_number_tuple(color1, "color1")
    r2, g2, b2 = _validate_rgb_number_tuple(color2, "color2")
    t = _validate_real(ratio, "ratio")
    if not 0.0 <= t <= 1.0:
        raise ValueError(f"ratio must be in the range [0, 1], got {ratio}.")
    if not isinstance(linear, bool):
        raise TypeError(f"linear must be a bool, got {type(linear).__name__}.")

    inv = 1.0 - t
    if linear:
        rl = _srgb_to_linear_channel(r1) * inv + _srgb_to_linear_channel(r2) * t
        gl = _srgb_to_linear_channel(g1) * inv + _srgb_to_linear_channel(g2) * t
        bl = _srgb_to_linear_channel(b1) * inv + _srgb_to_linear_channel(b2) * t
        return (
            max(0, min(255, round(_linear_to_srgb_channel(rl) * 255.0))),
            max(0, min(255, round(_linear_to_srgb_channel(gl) * 255.0))),
            max(0, min(255, round(_linear_to_srgb_channel(bl) * 255.0))),
        )

    return (
        max(0, min(255, round(r1 * inv + r2 * t))),
        max(0, min(255, round(g1 * inv + g2 * t))),
        max(0, min(255, round(b1 * inv + b2 * t))),
    )


def invert_color(rgb: Sequence[int]) -> tuple[int, int, int]:
    """Return the inverted sRGB color ``(255 - r, 255 - g, 255 - b)``.

    Parameters:
        rgb (tuple): Input RGB color ``(r, g, b)`` in ``[0, 255]``.

    Returns:
        tuple[int, int, int]: Inverted RGB color.
    """
    r, g, b = _validate_rgb_tuple(rgb)
    return 255 - r, 255 - g, 255 - b


def to_grayscale(rgb: Sequence[int]) -> tuple[int, int, int]:
    """Convert an RGB color to a perceptual grayscale RGB tuple.

    Computes relative luminance in linear sRGB and re-encodes using the sRGB
    transfer function so perceived brightness is faithfully preserved.

    Parameters:
        rgb (tuple): Input RGB color ``(r, g, b)`` in ``[0, 255]``.

    Returns:
        tuple[int, int, int]: Grayscale ``(v, v, v)`` tuple in ``[0, 255]``.
    """
    r, g, b = _validate_rgb_number_tuple(rgb)
    y_lin = (
        0.2126 * _srgb_to_linear_channel(r)
        + 0.7152 * _srgb_to_linear_channel(g)
        + 0.0722 * _srgb_to_linear_channel(b)
    )
    gray = max(0, min(255, round(_linear_to_srgb_channel(y_lin) * 255.0)))
    return gray, gray, gray


def adjust_lightness(rgb: Sequence[int], amount: float) -> tuple[int, int, int]:
    """Lighten or darken an RGB color by adjusting its HSL lightness.

    Parameters:
        rgb (tuple): Input RGB color ``(r, g, b)`` in ``[0, 255]``.
        amount (float): Signed delta in ``[-1, 1]`` added to HSL lightness
            (positive lightens, negative darkens; result clamped to ``[0, 1]``).

    Returns:
        tuple[int, int, int]: Adjusted RGB color in ``[0, 255]``.
    """
    r, g, b = _validate_rgb_number_tuple(rgb)
    delta = _validate_real(amount, "amount")
    if not -1.0 <= delta <= 1.0:
        raise ValueError(f"amount must be in the range [-1, 1], got {amount}.")
    h, s, l = _rgb_to_hsl_exact(r, g, b)
    new_l = max(0.0, min(1.0, l + delta))
    return hsl_to_rgb(h, s, new_l)


def adjust_saturation(rgb: Sequence[int], amount: float) -> tuple[int, int, int]:
    """Increase or decrease an RGB color's HSL saturation.

    Parameters:
        rgb (tuple): Input RGB color ``(r, g, b)`` in ``[0, 255]``.
        amount (float): Signed delta in ``[-1, 1]`` added to HSL saturation
            (positive saturates, negative desaturates; result clamped to ``[0, 1]``).

    Returns:
        tuple[int, int, int]: Adjusted RGB color in ``[0, 255]``.
    """
    r, g, b = _validate_rgb_number_tuple(rgb)
    delta = _validate_real(amount, "amount")
    if not -1.0 <= delta <= 1.0:
        raise ValueError(f"amount must be in the range [-1, 1], got {amount}.")
    h, s, l = _rgb_to_hsl_exact(r, g, b)
    new_s = max(0.0, min(1.0, s + delta))
    return hsl_to_rgb(h, new_s, l)
