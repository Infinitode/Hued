# Hued

[![PyPI Version](https://img.shields.io/pypi/v/hued.svg)](https://pypi.org/project/hued/)
[![Python Versions](https://img.shields.io/pypi/pyversions/hued.svg)](https://pypi.org/project/hued/)
[![CI](https://github.com/Infinitode/Hued/actions/workflows/ci.yml/badge.svg)](https://github.com/Infinitode/Hued/actions/workflows/ci.yml)
[![PyPI Trusted Publishing](https://img.shields.io/badge/PyPI-Trusted%20Publishing-006dad?logo=pypi&logoColor=white)](https://pypi.org/project/hued/)
[![PEP 740 Provenance](https://img.shields.io/badge/provenance-PEP%20740%20verified-brightgreen?logo=sigstore&logoColor=white)](https://pypi.org/project/hued/)
[![SLSA Build Provenance](https://img.shields.io/badge/SLSA-build%20provenance-brightgreen?logo=github&logoColor=white)](https://github.com/Infinitode/Hued/attestations)
[![Code Size](https://img.shields.io/github/languages/code-size/Infinitode/Hued)](https://github.com/Infinitode/Hued)
[![Downloads](https://pepy.tech/badge/hued)](https://pepy.tech/project/hued)
[![License Compliance](https://img.shields.io/badge/license-MIT%20(Modified)-brightgreen.svg)](LICENSE)

[Documentation](https://infinitode-docs.gitbook.io/documentation/package-documentation/hued-package-documentation) · [Changelog](CHANGELOG.md) · [PyPI](https://pypi.org/project/hued/)

An open-source, **zero-dependency** Python library for color space conversion, WCAG 2.1 accessibility analysis, perceptual color difference (CIEDE2000), color-blindness simulation, harmonious palette & gradient generation, and named color lookup.

## Changes in version 1.1.0

See [CHANGELOG.md](CHANGELOG.md) for the full list of fixes and additions.

- **Correctness & color-science fixes**:
  - Fixed `xyz_to_rgb` (and `xyz_to_*`) crashing with `complex` numbers on pure red, pure green, and other saturated colors; updated sRGB ↔ XYZ conversions to the exact IEC 61966-2-1 D65 specification for lossless round-trips.
  - Fixed `rgb_to_linear` and `get_luminance` to follow the exact IEC 61966-2-1 / WCAG 2.1 sRGB transfer function.
  - Fixed `get_text_color_from_background` returning unreadable text on black, charcoal, yellow, cyan, lime, and silver backgrounds — now guarantees maximum WCAG 2.1 contrast.
  - Fixed `check_color_quality` (previously always returned `True` for all 16.7M RGB colors), `simulate_color_blindness` (preserved exact neutral grays and linear luminance), `get_temperature`, `is_pastel`, `is_muted`, `hex_to_rgb` (added `#RGB` shorthand and strict validation), direct lossless `hsl_to_hsv`/`hsv_to_hsl`, `blend_colors`, and `ColorPalette` edge cases (`generate_monochromatic(1)`, `palette_to_hex()` on random palette dicts, rectangular `generate_tetradic()`, and `export_palette()` extension handling).
  - Cleaned the named color catalog (removed scraped citation/vandalism artifacts, resolved duplicate names, preserved acronym casing, and added all missing W3C CSS Level 4 named colors including `Green`, `Orange`, `Purple`, `Brown`, `Gold`, and `Lavender`).
- **New features**:
  - Full **CIE 1976 L\*a\*b\*** conversion suite (`rgb_to_lab`, `lab_to_rgb`, `hex_to_lab`, `lab_to_hex`, `xyz_to_lab`, `lab_to_xyz`, `hsl_to_lab`, `hsv_to_lab`, `cmyk_to_lab`, and inverses).
  - Perceptual color difference `delta_e` (**CIEDE2000** and **CIE76**) and full WCAG 2.1 report `check_wcag_contrast`.
  - Color utilities: `linear_to_rgb`, `invert_color`, `to_grayscale`, `adjust_lightness`, `adjust_saturation`, and linear-light `blend_colors(..., linear=True)`.
  - Perceptual closest-color matching (`space="lab"` / `"cie2000"`), `get_color_by_hex`, `search_colors`, `get_random_color`, `add_color`, and `remove_color` on `ColorManager`.
  - Perceptual gradients (`space="rgb" | "linear" | "lab" | "hsl"`) and `.css` custom-property export on `ColorPalette`.
  - Full inline type annotations (`py.typed`), modern `pyproject.toml`, automated test suite, and **PyPI Trusted Publishing** with **PEP 740** & **SLSA** build provenance attestations.

<details>
<summary>Earlier releases (1.0.3 – 1.0.7)</summary>

### Changes in version 1.0.7
- 2 new functions in `hued.analysis` for testing color visibility/quality and simulating color blindness.

### Changes in version 1.0.6
- New methods under `ColorPalette` to create gradients and export `ColorPalette` data as CSV, TXT, or JSON.

### Changes in version 1.0.5
- Conversion functions for `XYZ` / `CIE 1931 XYZ`.

### Changes in version 1.0.4
- Updated `colors.py` with 500+ additional color names.

### Changes in version 1.0.3
- Added `rgb_to_linear`, `get_luminance`, `get_vibrancy`, `color_contrast`, and `get_text_color_from_background` to `hued.analysis`.
- Added `blend_colors` and cross-format conversion helpers to `hued.conversions`.
- Added additional harmony schemes and random color generators to `ColorPalette`.

</details>

## Installation

```bash
pip install hued
```

**Supported Python versions:** Python **3.9+** (CI-tested across Python 3.10–3.14). Zero external runtime dependencies.

## Features

- **Color Conversions**: Lossless and validated conversions across **RGB**, **HEX** (`#RRGGBB` and `#RGB`), **HSL**, **HSV**, **CMYK**, **Linear sRGB**, **CIE 1931 XYZ (D65)**, and **CIE 1976 L\*a\*b\* (D65)**, plus blending, inversion, grayscale, lightness, and saturation adjustments.
- **Accessibility & Analysis**: WCAG 2.1 relative luminance, contrast ratios, AA/AAA compliance checks, optimal foreground text selection, CIEDE2000 / CIE76 perceptual color difference (`delta_e`), color-blindness simulation, and temperature/pastel/muted/vibrant classification.
- **Color Palettes & Gradients**: Complementary, split-complementary, analogous, triadic, rectangular tetradic, square, and monochromatic harmonies; multi-space gradients (`rgb`, `linear`, `lab`, `hsl`); export to `.json`, `.csv`, `.txt`, and `.css`.
- **Named Colors**: 1,300+ named colors (including all 148 W3C CSS Color Level 4 names) with exact lookup, CSS-token matching, substring search, and RGB / L\*a\*b\* / CIEDE2000 closest-color matching.
- **Fully Typed**: Ships a PEP 561 `py.typed` marker and complete inline annotations.

## Usage

### Named Colors

```python
from hued import ColorManager

cm = ColorManager()

blue = cm.get_color_by_name("Blue")
print(blue)  # {'Name': 'Blue', 'Hex': '#0000FF', 'RGB': (0, 0, 255)}

# Find the perceptually closest named color using CIEDE2000
print(cm.closest_color_name("#FF5733", space="cie2000"))

# Search and pick random named colors
print(len(cm.search_colors("cerulean")))
print(cm.get_random_color())
```

### Color Conversion & Manipulation

```python
from hued import (
    adjust_lightness,
    blend_colors,
    hex_to_rgb,
    rgb_to_hsl,
    rgb_to_lab,
)

rgb = hex_to_rgb("#FF5733")      # (255, 87, 51) — 3-digit '#F53' also works
hsl = rgb_to_hsl(*rgb)           # (10.59, 1.0, 0.6)
lab = rgb_to_lab(*rgb)           # CIE 1976 L*a*b* (D65)

mixed = blend_colors((255, 0, 0), (0, 255, 0), 0.5, linear=True)
lighter = adjust_lightness(rgb, 0.15)
```

### Accessibility, Contrast & Perceptual Analysis

```python
from hued import (
    check_wcag_contrast,
    delta_e,
    get_temperature,
    get_text_color_from_background,
    is_pastel,
    simulate_color_blindness,
)

print(is_pastel((255, 200, 200)))                      # True
print(get_temperature((255, 215, 0)))                  # 'Warm'
print(get_text_color_from_background((255, 255, 0)))   # 'dark'
print(check_wcag_contrast((20, 20, 20), (255, 255, 255)))
print(round(delta_e((255, 0, 0), (240, 15, 10)), 2))   # CIEDE2000
print(simulate_color_blindness((220, 50, 80), "deuteranopia"))
```

### Palettes, Gradients & Export

```python
from hued import ColorPalette

palette = ColorPalette((255, 60, 52))
print(palette.generate_complementary())
print(palette.generate_tetradic())  # Rectangular double-complementary

# Perceptually smooth gradient in CIE L*a*b* space
gradient = palette.generate_gradient((255, 60, 52), (51, 247, 255), steps=5, space="lab")

# Export palettes to .json, .csv, .txt, or .css
palette.export_palette("palette.css")
```

## Release Provenance & Verification

Releases of `hued` are published directly from GitHub Actions using **PyPI OIDC Trusted Publishing** (no long-lived API tokens) with automatic **PEP 740** digital provenance attestations on [PyPI](https://pypi.org/project/hued/) and **SLSA v1.0** build provenance attestations on [GitHub](https://github.com/Infinitode/Hued/attestations).

You can verify any downloaded distribution artifact with the GitHub CLI:

```bash
gh attestation verify hued-*.whl --repo Infinitode/Hued
```

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and testing instructions, or open an issue / pull request on [GitHub](https://github.com/Infinitode/Hued).

## License

Hued is released under the terms of the **MIT License (Modified)**. See [LICENSE](LICENSE) for the full text.

**Modified License Clause:** Derivative works based on Hued are permitted provided that any substantial changes are clearly distinguished from the original work and distributed under a different name.
