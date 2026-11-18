# Changelog

All notable changes to **Hued** are documented in this file.

## [1.1.0] - 2026-11-18

A full correctness, color-science accuracy, performance, and supply-chain security release.

### Fixed
- **`xyz_to_rgb` & all `xyz_to_*` conversions**: Fixed a `TypeError` crash caused by raising tiny negative linear channels (e.g. pure red `(255, 0, 0)` and pure green `(0, 255, 0)`) to a fractional power and producing `complex` numbers before clamping. Updated forward and inverse transformations to the standard IEC 61966-2-1 sRGB D65 matrix and companding curves for exact lossless round-trips across all sRGB colors.
- **`rgb_to_linear` & `get_luminance`**: Fixed a dead-code threshold bug (`c > 0.04045` compared against `[0, 255]` instead of normalized `c / 255`) and replaced the gamma `2.2` approximation with the exact IEC 61966-2-1 / WCAG 2.1 sRGB transfer function (`((s + 0.055) / 1.055) ** 2.4` above `0.04045`, `s / 12.92` otherwise).
- **`get_text_color_from_background`**: Fixed inverted accessibility recommendations that returned `"dark"` text on pure black `(0, 0, 0)` and charcoal backgrounds, and `"light"` text on pure yellow `(255, 255, 0)`, cyan `(0, 255, 255)`, lime `(0, 255, 0)`, and light silver `(180, 180, 180)`. Now always selects whichever of light or dark text maximizes WCAG 2.1 contrast.
- **`check_color_quality`**: Fixed a mathematical tautology where `is_good_quality` could never return `False` (`max(contrast_black, contrast_white) >= sqrt(21) ≈ 4.58 > 4.5` for all 16.7M RGB colors). Now defaults to WCAG AAA (`7.0`) when evaluating against black/white generically, and to WCAG AA (`4.5`) when evaluating against a specific `background`, while reporting explicit AA/AAA flags for both black and white.
- **`simulate_color_blindness`**: Fixed floating-point `int()` truncation and gamma drift that shifted neutral grays; updated achromatopsia weights to linear sRGB luminance (`0.2126, 0.7152, 0.0722`) and interpolated severity in linear sRGB space.
- **`get_temperature`, `is_pastel`, & `is_muted`**:
  - `get_temperature` now correctly classifies yellow as `"Warm"`, cyan and teal as `"Cool"`, and near-grays as `"Neutral"`.
  - `is_pastel` no longer misclassifies pure white `(255, 255, 255)` or light grays as pastel, and now recognizes soft pastels such as pastel green `(119, 221, 119)`.
  - `is_muted` no longer misclassifies pure black `(0, 0, 0)` as muted, supports mid-lightness muted shades (e.g. sage green, dusty rose), and no longer shadows `brightness`.
- **`hex_to_rgb` & `rgb_to_hex`**: Fixed silent acceptance of malformed hex strings (`"##FF0000"`, `"#12345"`, `"#FF0000EXTRA"`, `"#+1+2+3"`) and out-of-range/boolean RGB values (`rgb_to_hex(-1, 0, 0)` → `"#-10000"`, `rgb_to_hex(256, 0, 0)` → `"#1000000"`). Added support for 3-digit shorthand hex codes (`"#FFF"`) and surrounding whitespace.
- **`hsl_to_hsv` & `hsv_to_hsl`**: Replaced lossy 8-bit RGB round-trips with direct analytical conversions, eliminating hue quantization drift. Enforced consistent input validation across all HSL, HSV, CMYK, XYZ, and LAB conversions, and prevented rounded hues from ever reaching `360.0`.
- **`blend_colors` & `ColorPalette.generate_gradient`**: Replaced `int()` truncation with `round()` so blending a color with itself always returns the exact input color, and added range validation for `ratio` and RGB channels.
- **`ColorPalette`**:
  - Fixed `ZeroDivisionError` in `generate_monochromatic(shades=1)` and rejected `shades < 1`.
  - Differentiated `generate_tetradic(angle=60)` (rectangular double-complementary) from `generate_square()` (`90°`).
  - Fixed `TypeError` in `palette_to_hex()` when called after `generate_random_palette()`.
  - Fixed `export_palette()` file-extension parsing (`os.path.splitext`) so extensionless filenames like `"json"` are rejected and dotted directory paths work; removed unsolicited `print()` output on errors.
- **`ColorManager` & named color catalog**:
  - Removed a scraped Wikipedia vandalism entry and cleaned citation markers (`"Cinnamon[citation needed]"` → `"Cinnamon"`, `"Heidelberg Red[2]"` → `"Heidelberg Red"`).
  - Disambiguated 7 duplicate color names that made secondary entries unreachable and normalized all hex strings to uppercase `#RRGGBB`.
  - Preserved acronyms and apostrophes in `get_color_by_name()` (e.g. `"Air Force blue (RAF)"`, `"B'dazzled blue"`) instead of corrupting them with `.title()`.
  - Added 21 missing W3C CSS named colors (`Green`, `Orange`, `Purple`, `Brown`, `Gold`, `Lavender`, `Lime`, `Maroon`, `Khaki`, `Chocolate`, `Chartreuse`, `Forest green`, `Olive drab`, `Dark gray`, and `Grey` spellings) plus hyphen/space-insensitive lookup so all 148 standard CSS Color Level 4 named colors resolve.
- **Packaging**: Migrated from broken `{{VERSION_PLACEHOLDER}}` `setup.py` to standards-compliant PEP 621 `pyproject.toml` (Python `>=3.9`), fixing local `pip install .` and `python -m build`.

### Added
- **CIE 1976 L\*a\*b\* conversions**: `rgb_to_lab`, `lab_to_rgb`, `xyz_to_lab`, `lab_to_xyz`, `hex_to_lab`, `lab_to_hex`, `hsl_to_lab`, `lab_to_hsl`, `hsv_to_lab`, `lab_to_hsv`, `cmyk_to_lab`, `lab_to_cmyk`.
- **Color adjustment helpers**: `linear_to_rgb`, `invert_color`, `to_grayscale`, `adjust_lightness`, `adjust_saturation`, and gamma-correct `blend_colors(..., linear=True)`.
- **Perceptual difference & accessibility**: `delta_e(color1, color2, method="cie2000" | "cie76")` (validated against Sharma, Wu & Dalal 2005 CIEDE2000 test vectors) and `check_wcag_contrast(foreground, background)`.
- **Richer `ColorManager` API**: `closest_color_name(..., space="rgb" | "lab" | "cie2000")`, `get_color_by_hex`, `search_colors`, `get_random_color`, `add_color`, `remove_color`, plus module-level RGB/LAB caching.
- **Enhanced `ColorPalette` API**: Multi-space gradients (`space="rgb" | "linear" | "lab" | "hsl"`), `.css` custom-properties export, `pathlib.Path` support, and configurable `angle` on `generate_tetradic` and `generate_split_complementary`.
- **Static typing & metadata**: Full inline type annotations, PEP 561 `py.typed` marker, `hued.__version__`, and explicit `__all__` across all modules.
- **CI & Supply-Chain Provenance**: Multi-version GitHub Actions CI (`ci.yml`) and OIDC Trusted Publishing (`build_and_publish.yml`) with PEP 740 PyPI digital attestations and GitHub SLSA build provenance attestations.

## [1.0.7] and earlier

See `readme.md` and the [GitHub Releases](https://github.com/Infinitode/Hued/releases) history for versions `1.0.0` through `1.0.7`.
