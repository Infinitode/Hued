"""Color palette harmony generation, gradients, random sampling, and file export."""

from __future__ import annotations

import csv
import json
import os
import random
import re
from collections.abc import Sequence
from typing import Any

from hued.conversions import (
    _linear_to_srgb_channel,
    _rgb_to_hsl_exact,
    _srgb_to_linear_channel,
    _validate_real,
    _validate_rgb_tuple,
    _wrap_hue,
    hsl_to_rgb,
    lab_to_rgb,
    rgb_to_hex,
    rgb_to_hsl,
    rgb_to_lab,
)

__all__ = ["ColorPalette"]

_SUPPORTED_EXPORT_EXTENSIONS = {".json", ".txt", ".csv", ".css"}
_CSS_SLUG_RE = re.compile(r"[^a-z0-9]+")


def _is_rgb_color(value: Any) -> bool:
    """Return True if ``value`` is a valid 3-channel integer RGB tuple."""
    return (
        isinstance(value, tuple)
        and len(value) == 3
        and all(isinstance(c, int) and not isinstance(c, bool) and 0 <= c <= 255 for c in value)
    )


def _css_slug(label: str) -> str:
    return _CSS_SLUG_RE.sub("-", label.strip().lower()).strip("-") or "color"


class ColorPalette:
    """Create, manipulate, and export harmonious color palettes.

    Attributes:
        base_color (tuple[int, int, int]): Base RGB color ``(r, g, b)`` in ``[0, 255]``.
        palette (list | dict): Current palette — a list of RGB tuples for single
            harmony schemes, or a dictionary of schemes after
            :meth:`generate_random_palette`.
    """

    def __init__(self, base_color: Sequence[int]) -> None:
        """Initialize the palette with an RGB base color in ``[0, 255]``."""
        validated = _validate_rgb_tuple(base_color, "base_color")
        self.base_color: tuple[int, int, int] = validated
        self.palette: list[tuple[int, int, int]] | dict[str, Any] = [validated]

    def generate_complementary(self) -> list[tuple[int, int, int]]:
        """Generate a 2-color complementary palette (``0°``, ``+180°``)."""
        h, s, l = rgb_to_hsl(*self.base_color)
        complementary_color = hsl_to_rgb(_wrap_hue(h + 180.0), s, l)
        self.palette = [self.base_color, complementary_color]
        return self.palette

    def generate_analogous(self, angle: float = 30) -> list[tuple[int, int, int]]:
        """Generate a 3-color analogous palette (``-angle``, ``0°``, ``+angle``).

        Parameters:
            angle (float): Hue separation in degrees (default ``30``).
        """
        step = _validate_real(angle, "angle")
        if not 0.0 < step < 180.0:
            raise ValueError(f"angle must be in (0, 180), got {angle}.")
        h, s, l = rgb_to_hsl(*self.base_color)
        analogous1 = hsl_to_rgb(_wrap_hue(h + step), s, l)
        analogous2 = hsl_to_rgb(_wrap_hue(h - step), s, l)
        self.palette = [analogous2, self.base_color, analogous1]
        return self.palette

    def generate_triadic(self) -> list[tuple[int, int, int]]:
        """Generate a 3-color triadic palette (``0°``, ``+120°``, ``+240°``)."""
        h, s, l = rgb_to_hsl(*self.base_color)
        triadic1 = hsl_to_rgb(_wrap_hue(h + 120.0), s, l)
        triadic2 = hsl_to_rgb(_wrap_hue(h - 120.0), s, l)
        self.palette = [self.base_color, triadic1, triadic2]
        return self.palette

    def generate_monochromatic(self, shades: int = 24) -> list[tuple[int, int, int]]:
        """Generate a monochromatic palette of varying lightness levels.

        Parameters:
            shades (int): Number of lightness steps to sample (must be ``>= 1``,
                default ``24``). Clamped duplicate lightness values are omitted.
        """
        if isinstance(shades, bool) or not isinstance(shades, int):
            raise TypeError(f"shades must be an integer, got {type(shades).__name__}.")
        if shades < 1:
            raise ValueError(f"shades must be at least 1, got {shades}.")

        if shades == 1:
            self.palette = [self.base_color]
            return self.palette

        h, s, l = rgb_to_hsl(*self.base_color)
        lightness_values: list[float] = []
        for i in range(shades):
            new_lightness = max(min(l + (i / (shades - 1)) - 0.5, 1.0), 0.0)
            if new_lightness not in lightness_values:
                lightness_values.append(new_lightness)

        self.palette = [hsl_to_rgb(h, s, lightness) for lightness in lightness_values]
        return self.palette

    def generate_tetradic(self, angle: float = 60) -> list[tuple[int, int, int]]:
        """Generate a 4-color rectangular tetradic (double-complementary) palette.

        Produces colors at hue offsets ``0°``, ``+angle``, ``+180°``, and
        ``+(180° + angle)``. With default ``angle=60`` this forms a classic
        rectangular tetrad distinct from :meth:`generate_square` (``angle=90``).

        Parameters:
            angle (float): Separation between paired hues in ``(0, 180)``
                (default ``60``).
        """
        step = _validate_real(angle, "angle")
        if not 0.0 < step < 180.0:
            raise ValueError(f"angle must be in (0, 180), got {angle}.")

        h, s, l = rgb_to_hsl(*self.base_color)
        tetradic1 = hsl_to_rgb(_wrap_hue(h + step), s, l)
        tetradic2 = hsl_to_rgb(_wrap_hue(h + 180.0), s, l)
        tetradic3 = hsl_to_rgb(_wrap_hue(h + 180.0 + step), s, l)

        self.palette = [self.base_color, tetradic1, tetradic2, tetradic3]
        return self.palette

    def generate_square(self) -> list[tuple[int, int, int]]:
        """Generate a 4-color square palette (``0°``, ``+90°``, ``+180°``, ``+270°``)."""
        h, s, l = rgb_to_hsl(*self.base_color)
        square1 = hsl_to_rgb(_wrap_hue(h + 90.0), s, l)
        square2 = hsl_to_rgb(_wrap_hue(h + 180.0), s, l)
        square3 = hsl_to_rgb(_wrap_hue(h + 270.0), s, l)

        self.palette = [self.base_color, square1, square2, square3]
        return self.palette

    def generate_split_complementary(self, angle: float = 30) -> list[tuple[int, int, int]]:
        """Generate a 3-color split-complementary palette.

        Parameters:
            angle (float): Offset in degrees on each side of the complement
                (default ``30``, giving ``+150°`` and ``+210°``).
        """
        step = _validate_real(angle, "angle")
        if not 0.0 < step < 180.0:
            raise ValueError(f"angle must be in (0, 180), got {angle}.")

        h, s, l = rgb_to_hsl(*self.base_color)
        split_comp1 = hsl_to_rgb(_wrap_hue(h + 180.0 - step), s, l)
        split_comp2 = hsl_to_rgb(_wrap_hue(h + 180.0 + step), s, l)

        self.palette = [self.base_color, split_comp1, split_comp2]
        return self.palette

    def palette_to_hex(self) -> list[str] | dict[str, Any]:
        """Convert the current palette to uppercase ``#RRGGBB`` hex strings.

        Returns a ``list[str]`` when ``self.palette`` is a list of RGB tuples,
        or a ``dict`` mirroring the keys of ``self.palette`` when it was
        populated by :meth:`generate_random_palette`.
        """
        if isinstance(self.palette, list):
            return [rgb_to_hex(*_validate_rgb_tuple(color, "color")) for color in self.palette]
        if isinstance(self.palette, dict):
            converted: dict[str, Any] = {}
            for key, value in self.palette.items():
                if _is_rgb_color(value):
                    converted[key] = rgb_to_hex(*value)
                elif isinstance(value, list):
                    converted[key] = [
                        rgb_to_hex(*_validate_rgb_tuple(color, "color")) for color in value
                    ]
                else:
                    converted[key] = value
            return converted
        raise TypeError(
            f"Unsupported palette type: {type(self.palette).__name__}. Must be list or dict."
        )

    def add_color(self, rgb_color: Sequence[int]) -> None:
        """Append a validated RGB color to a list-based palette.

        Raises:
            TypeError: If ``rgb_color`` is invalid or ``self.palette`` is currently a dict.
            ValueError: If RGB channel values are outside ``[0, 255]``.
        """
        validated = _validate_rgb_tuple(rgb_color, "rgb_color")
        if not isinstance(self.palette, list):
            raise TypeError(
                "Cannot add a color when palette is a dictionary. "
                "Generate a list-based palette first or use set_as_current=False."
            )
        self.palette.append(validated)

    def remove_color(self, rgb_color: Sequence[int]) -> None:
        """Remove a validated RGB color from a list-based palette if present.

        Raises:
            TypeError: If ``rgb_color`` is invalid or ``self.palette`` is currently a dict.
            ValueError: If RGB channel values are outside ``[0, 255]``.
        """
        validated = _validate_rgb_tuple(rgb_color, "rgb_color")
        if not isinstance(self.palette, list):
            raise TypeError(
                "Cannot remove a color when palette is a dictionary. "
                "Generate a list-based palette first or use set_as_current=False."
            )
        if validated in self.palette:
            self.palette.remove(validated)

    def generate_random_palette(self, set_as_current: bool = True) -> dict[str, Any]:
        """Generate a random base color and all harmony palettes as a dictionary.

        Parameters:
            set_as_current (bool): If ``True`` (default), update ``self.base_color``
                and set ``self.palette`` to the returned dictionary. If ``False``,
                leave instance state unchanged.
        """
        if not isinstance(set_as_current, bool):
            raise TypeError(
                f"set_as_current must be a bool, got {type(set_as_current).__name__}."
            )

        random_base_color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )

        original_base = self.base_color
        original_palette = self.palette
        self.base_color = random_base_color

        try:
            palette_dict: dict[str, Any] = {
                "Base Color": random_base_color,
                "Complementary Palette": self.generate_complementary(),
                "Analogous Palette": self.generate_analogous(),
                "Triadic Palette": self.generate_triadic(),
                "Monochromatic Palette": self.generate_monochromatic(),
                "Tetradic Palette": self.generate_tetradic(),
                "Square Palette": self.generate_square(),
                "Split Complementary Palette": self.generate_split_complementary(),
            }
        except Exception:
            self.base_color = original_base
            self.palette = original_palette
            raise

        if set_as_current:
            self.palette = palette_dict
        else:
            self.base_color = original_base
            self.palette = original_palette

        return palette_dict

    def generate_random_color(self) -> dict[str, Any]:
        """Generate a random color returned in RGB, HEX, and HSL formats."""
        base_color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )
        return {
            "RGB Color": base_color,
            "HEX Color": rgb_to_hex(*base_color),
            "HSL Color": rgb_to_hsl(*base_color),
        }

    def generate_random_hex_colors(self, n: int = 10) -> list[str]:
        """Generate ``n`` random uppercase ``#RRGGBB`` color codes."""
        if isinstance(n, bool) or not isinstance(n, int):
            raise TypeError(f"n must be an integer, got {type(n).__name__}.")
        if n < 0:
            raise ValueError(f"n must be non-negative, got {n}.")
        return [self.generate_random_color()["HEX Color"] for _ in range(n)]

    def generate_gradient(
        self,
        color1: Sequence[int],
        color2: Sequence[int],
        steps: int = 10,
        *,
        space: str = "rgb",
    ) -> list[tuple[int, int, int]]:
        """Generate a smooth gradient between two RGB colors (``steps + 1`` stops).

        Does not modify ``self.palette``.

        Parameters:
            color1 (tuple): Starting RGB color ``(r, g, b)`` in ``[0, 255]``.
            color2 (tuple): Ending RGB color ``(r, g, b)`` in ``[0, 255]``.
            steps (int): Number of intervals (``>= 1``; returns ``steps + 1`` colors).
            space (str): Interpolation color space — ``"rgb"`` (default),
                ``"linear"`` (gamma-correct linear sRGB), ``"lab"`` (perceptually
                uniform CIE L*a*b*), or ``"hsl"`` (shortest-arc hue).

        Returns:
            list[tuple[int, int, int]]: Gradient stops starting at ``color1`` and
            ending at ``color2``.
        """
        c1 = _validate_rgb_tuple(color1, "color1")
        c2 = _validate_rgb_tuple(color2, "color2")
        if isinstance(steps, bool) or not isinstance(steps, int):
            raise TypeError(f"steps must be an integer, got {type(steps).__name__}.")
        if steps < 1:
            raise ValueError("Number of steps must be at least 1.")
        if not isinstance(space, str):
            raise TypeError(f"space must be a string, got {type(space).__name__}.")

        mode = space.strip().lower()
        if mode not in {"rgb", "linear", "lab", "hsl"}:
            raise ValueError(
                f"Unknown gradient color space {space!r}. Use 'rgb', 'linear', 'lab', or 'hsl'."
            )

        gradient: list[tuple[int, int, int]] = []

        if mode == "rgb":
            for i in range(steps + 1):
                ratio = i / steps
                inv = 1.0 - ratio
                r = max(0, min(255, round(c1[0] * inv + c2[0] * ratio)))
                g = max(0, min(255, round(c1[1] * inv + c2[1] * ratio)))
                b = max(0, min(255, round(c1[2] * inv + c2[2] * ratio)))
                gradient.append((r, g, b))
            return gradient

        if mode == "linear":
            lin1 = tuple(_srgb_to_linear_channel(ch) for ch in c1)
            lin2 = tuple(_srgb_to_linear_channel(ch) for ch in c2)
            for i in range(steps + 1):
                ratio = i / steps
                inv = 1.0 - ratio
                rgb = (
                    max(0, min(255, round(_linear_to_srgb_channel(lin1[0] * inv + lin2[0] * ratio) * 255.0))),
                    max(0, min(255, round(_linear_to_srgb_channel(lin1[1] * inv + lin2[1] * ratio) * 255.0))),
                    max(0, min(255, round(_linear_to_srgb_channel(lin1[2] * inv + lin2[2] * ratio) * 255.0))),
                )
                gradient.append(rgb)
            return gradient

        if mode == "lab":
            lab1 = rgb_to_lab(*c1)
            lab2 = rgb_to_lab(*c2)
            for i in range(steps + 1):
                if i == 0:
                    gradient.append(c1)
                elif i == steps:
                    gradient.append(c2)
                else:
                    ratio = i / steps
                    inv = 1.0 - ratio
                    l_val = lab1[0] * inv + lab2[0] * ratio
                    a_val = lab1[1] * inv + lab2[1] * ratio
                    b_val = lab1[2] * inv + lab2[2] * ratio
                    gradient.append(lab_to_rgb(l_val, a_val, b_val))
            return gradient

        # mode == "hsl" (shortest-arc hue interpolation; preserve hue for achromatic endpoints)
        h1, s1, l1 = _rgb_to_hsl_exact(*c1)
        h2, s2, l2 = _rgb_to_hsl_exact(*c2)
        if s1 == 0.0 and s2 > 0.0:
            h1 = h2
        elif s2 == 0.0 and s1 > 0.0:
            h2 = h1
        dh = ((h2 - h1 + 540.0) % 360.0) - 180.0

        for i in range(steps + 1):
            if i == 0:
                gradient.append(c1)
            elif i == steps:
                gradient.append(c2)
            else:
                ratio = i / steps
                inv = 1.0 - ratio
                h_val = _wrap_hue(h1 + dh * ratio)
                s_val = max(0.0, min(1.0, s1 * inv + s2 * ratio))
                l_val = max(0.0, min(1.0, l1 * inv + l2 * ratio))
                gradient.append(hsl_to_rgb(h_val, s_val, l_val))
        return gradient

    def _format_color_output(self, color_tuple: Sequence[int]) -> dict[str, Any]:
        """Format a validated RGB tuple for export."""
        rgb = _validate_rgb_tuple(color_tuple, "color")
        return {"rgb": rgb, "hex": rgb_to_hex(*rgb)}

    def export_palette(self, filename: str | os.PathLike[str] = "palette.json") -> None:
        """Export the current palette (list or dictionary) to disk.

        Supported file extensions: ``.json``, ``.txt``, ``.csv``, and ``.css``.

        Parameters:
            filename (str | os.PathLike): Destination path whose extension selects
                the output format (default ``"palette.json"``).

        Raises:
            TypeError: If ``filename`` or ``self.palette`` has an unsupported type.
            ValueError: If ``self.palette`` is empty or ``filename`` has an
                unsupported/missing extension.
        """
        if not isinstance(filename, (str, os.PathLike)):
            raise TypeError(
                f"filename must be a string or PathLike, got {type(filename).__name__}."
            )
        if not isinstance(self.palette, (list, dict)):
            raise TypeError(
                f"Unsupported palette type: {type(self.palette).__name__}. Must be list or dict."
            )
        if not self.palette:
            raise ValueError("Palette is empty, cannot export.")

        path_str = os.fspath(filename)
        file_ext = os.path.splitext(path_str)[1].lower()
        if file_ext not in _SUPPORTED_EXPORT_EXTENSIONS:
            raise ValueError("Unsupported file format. Use .json, .txt, .csv, or .css.")

        if isinstance(self.palette, list):
            formatted_list = [self._format_color_output(color) for color in self.palette]
            if file_ext == ".json":
                export_list = [
                    {"rgb": list(item["rgb"]), "hex": item["hex"]} for item in formatted_list
                ]
                with open(path_str, "w", encoding="utf-8") as f:
                    json.dump(export_list, f, indent=4)
            elif file_ext == ".txt":
                with open(path_str, "w", encoding="utf-8") as f:
                    f.write("--- Simple Palette ---\n")
                    for i, item in enumerate(formatted_list):
                        f.write(f"{i}: {item['hex']} - RGB{item['rgb']}\n")
            elif file_ext == ".csv":
                with open(path_str, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Type", "Index", "Hex", "R", "G", "B"])
                    for i, item in enumerate(formatted_list):
                        r, g, b = item["rgb"]
                        writer.writerow(["Simple Palette", i, item["hex"], r, g, b])
            elif file_ext == ".css":
                with open(path_str, "w", encoding="utf-8") as f:
                    f.write(":root {\n")
                    for i, item in enumerate(formatted_list):
                        f.write(f"  --palette-color-{i}: {item['hex']};\n")
                    f.write("}\n")
            return

        # Dictionary palette export
        if file_ext == ".json":
            export_dict: dict[str, Any] = {}
            for key, value in self.palette.items():
                if _is_rgb_color(value):
                    item = self._format_color_output(value)
                    export_dict[key] = {"rgb": list(item["rgb"]), "hex": item["hex"]}
                elif isinstance(value, list):
                    export_dict[key] = [
                        {"rgb": list(item["rgb"]), "hex": item["hex"]}
                        for item in (self._format_color_output(c) for c in value)
                    ]
                else:
                    export_dict[key] = value
            with open(path_str, "w", encoding="utf-8") as f:
                json.dump(export_dict, f, indent=4)
        elif file_ext == ".txt":
            with open(path_str, "w", encoding="utf-8") as f:
                for key, value in self.palette.items():
                    f.write(f"--- {key} ---\n")
                    if _is_rgb_color(value):
                        item = self._format_color_output(value)
                        f.write(f"0: {item['hex']} - RGB{item['rgb']}\n")
                    elif isinstance(value, list):
                        for i, color in enumerate(value):
                            item = self._format_color_output(color)
                            f.write(f"{i}: {item['hex']} - RGB{item['rgb']}\n")
                    else:
                        f.write(f"{value}\n")
                    f.write("\n")
        elif file_ext == ".csv":
            with open(path_str, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["PaletteName", "Index", "Hex", "R", "G", "B"])
                for key, value in self.palette.items():
                    if _is_rgb_color(value):
                        item = self._format_color_output(value)
                        r, g, b = item["rgb"]
                        writer.writerow([key, 0, item["hex"], r, g, b])
                    elif isinstance(value, list):
                        for i, color in enumerate(value):
                            item = self._format_color_output(color)
                            r, g, b = item["rgb"]
                            writer.writerow([key, i, item["hex"], r, g, b])
        elif file_ext == ".css":
            with open(path_str, "w", encoding="utf-8") as f:
                f.write(":root {\n")
                for key, value in self.palette.items():
                    slug = _css_slug(str(key))
                    if _is_rgb_color(value):
                        item = self._format_color_output(value)
                        f.write(f"  --{slug}: {item['hex']};\n")
                    elif isinstance(value, list):
                        for i, color in enumerate(value):
                            item = self._format_color_output(color)
                            f.write(f"  --{slug}-{i}: {item['hex']};\n")
                f.write("}\n")
