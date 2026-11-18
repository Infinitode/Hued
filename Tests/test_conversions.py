"""Comprehensive unit tests for hued.conversions."""

from __future__ import annotations

import math

import pytest

import hued
from hued.analysis import rgb_to_linear
from hued.conversions import (
    adjust_lightness,
    adjust_saturation,
    blend_colors,
    cmyk_to_hex,
    cmyk_to_hsl,
    cmyk_to_hsv,
    cmyk_to_lab,
    cmyk_to_rgb,
    cmyk_to_xyz,
    hex_to_cmyk,
    hex_to_hsl,
    hex_to_hsv,
    hex_to_lab,
    hex_to_rgb,
    hex_to_xyz,
    hsl_to_cmyk,
    hsl_to_hex,
    hsl_to_hsv,
    hsl_to_lab,
    hsl_to_rgb,
    hsl_to_xyz,
    hsv_to_cmyk,
    hsv_to_hex,
    hsv_to_hsl,
    hsv_to_lab,
    hsv_to_rgb,
    hsv_to_xyz,
    invert_color,
    lab_to_cmyk,
    lab_to_hex,
    lab_to_hsl,
    lab_to_hsv,
    lab_to_rgb,
    lab_to_xyz,
    linear_to_rgb,
    rgb_to_cmyk,
    rgb_to_hex,
    rgb_to_hsl,
    rgb_to_hsv,
    rgb_to_lab,
    rgb_to_xyz,
    to_grayscale,
    xyz_to_cmyk,
    xyz_to_hex,
    xyz_to_hsl,
    xyz_to_hsv,
    xyz_to_lab,
    xyz_to_rgb,
)


class TestHexRgb:
    @pytest.mark.parametrize(
        ("rgb", "expected"),
        [
            ((255, 0, 0), "#FF0000"),
            ((0, 255, 0), "#00FF00"),
            ((0, 0, 255), "#0000FF"),
            ((0, 0, 0), "#000000"),
            ((255, 255, 255), "#FFFFFF"),
            ((15, 16, 171), "#0F10AB"),
        ],
    )
    def test_rgb_to_hex_valid(self, rgb: tuple[int, int, int], expected: str) -> None:
        assert rgb_to_hex(*rgb) == expected

    @pytest.mark.parametrize("bad", [(-1, 0, 0), (256, 0, 0), (0, -5, 0), (0, 0, 999)])
    def test_rgb_to_hex_out_of_range(self, bad: tuple[int, int, int]) -> None:
        with pytest.raises(ValueError):
            rgb_to_hex(*bad)

    @pytest.mark.parametrize(
        "bad",
        [(12.5, 0, 0), (True, 0, 0), (0, False, 0), ("255", 0, 0)],  # type: ignore[list-item]
    )
    def test_rgb_to_hex_invalid_type(self, bad: tuple[object, object, object]) -> None:
        with pytest.raises(TypeError):
            rgb_to_hex(*bad)  # type: ignore[arg-type]

    @pytest.mark.parametrize(
        ("hex_str", "expected"),
        [
            ("#00FF00", (0, 255, 0)),
            ("FF0000", (255, 0, 0)),
            ("#ff5733", (255, 87, 51)),
            ("  #0f10ab  ", (15, 16, 171)),
            ("#FFF", (255, 255, 255)),
            ("#000", (0, 0, 0)),
            ("f0a", (255, 0, 170)),
        ],
    )
    def test_hex_to_rgb_valid(self, hex_str: str, expected: tuple[int, int, int]) -> None:
        assert hex_to_rgb(hex_str) == expected

    @pytest.mark.parametrize(
        "bad_hex",
        [
            "",
            "#",
            "##FF0000",
            "#12",
            "#1234",
            "#12345",
            "#FF000080",
            "#FF0000EXTRA",
            "#GGGGGG",
            "#+1+2+3",
            "#-10000",
            "#12 345",
        ],
    )
    def test_hex_to_rgb_rejects_malformed(self, bad_hex: str) -> None:
        with pytest.raises(ValueError):
            hex_to_rgb(bad_hex)

    def test_hex_to_rgb_rejects_non_string(self) -> None:
        with pytest.raises(TypeError):
            hex_to_rgb(0xFF0000)  # type: ignore[arg-type]


class TestHslHsvCmyk:
    @pytest.mark.parametrize(
        ("rgb", "hsl"),
        [
            ((255, 0, 0), (0.0, 1.0, 0.5)),
            ((255, 255, 0), (60.0, 1.0, 0.5)),
            ((0, 255, 0), (120.0, 1.0, 0.5)),
            ((0, 255, 255), (180.0, 1.0, 0.5)),
            ((0, 0, 255), (240.0, 1.0, 0.5)),
            ((255, 0, 255), (300.0, 1.0, 0.5)),
            ((0, 0, 0), (0.0, 0.0, 0.0)),
            ((255, 255, 255), (0.0, 0.0, 1.0)),
            ((128, 128, 128), (0.0, 0.0, 0.5)),
        ],
    )
    def test_rgb_hsl_roundtrip_primaries(
        self, rgb: tuple[int, int, int], hsl: tuple[float, float, float]
    ) -> None:
        assert rgb_to_hsl(*rgb) == hsl
        if rgb != (128, 128, 128):
            assert hsl_to_rgb(*hsl) == rgb

    def test_hue_never_rounds_to_360(self) -> None:
        # Float RGB where raw hue is 359.9976...; rounding must wrap to 0.0, never 360.0.
        h_hsl, _, _ = rgb_to_hsl(255, 0, 0.01)  # type: ignore[arg-type]
        h_hsv, _, _ = rgb_to_hsv(255, 0, 0.01)  # type: ignore[arg-type]
        assert h_hsl == 0.0
        assert h_hsv == 0.0
        assert hsl_to_hex((h_hsl, 1.0, 0.5)) == "#FF0000"

    @pytest.mark.parametrize(
        "bad_hsl",
        [(360, 1, 0.5), (-1, 1, 0.5), (120, 1.1, 0.5), (120, -0.1, 0.5), (120, 0.5, 1.2), (math.nan, 0.5, 0.5)],
    )
    def test_hsl_validation(self, bad_hsl: tuple[float, float, float]) -> None:
        with pytest.raises(ValueError):
            hsl_to_rgb(*bad_hsl)
        with pytest.raises(ValueError):
            hsl_to_hex(bad_hsl)
        with pytest.raises(ValueError):
            hsl_to_xyz(bad_hsl)

    @pytest.mark.parametrize(
        ("rgb", "hsv"),
        [
            ((255, 0, 0), (0.0, 1.0, 1.0)),
            ((255, 255, 0), (60.0, 1.0, 1.0)),
            ((0, 255, 0), (120.0, 1.0, 1.0)),
            ((0, 255, 255), (180.0, 1.0, 1.0)),
            ((0, 0, 255), (240.0, 1.0, 1.0)),
            ((255, 0, 255), (300.0, 1.0, 1.0)),
            ((0, 0, 0), (0.0, 0.0, 0.0)),
            ((255, 255, 255), (0.0, 0.0, 1.0)),
        ],
    )
    def test_rgb_hsv_roundtrip_primaries(
        self, rgb: tuple[int, int, int], hsv: tuple[float, float, float]
    ) -> None:
        assert rgb_to_hsv(*rgb) == hsv
        assert hsv_to_rgb(*hsv) == rgb

    @pytest.mark.parametrize(
        "bad_hsv",
        [(360, 1, 1), (-5, 1, 1), (0, 2, 1), (0, 1, -0.1), (math.inf, 0.5, 0.5)],
    )
    def test_hsv_validation(self, bad_hsv: tuple[float, float, float]) -> None:
        with pytest.raises(ValueError):
            hsv_to_rgb(*bad_hsv)
        with pytest.raises(ValueError):
            hsv_to_hex(bad_hsv)
        with pytest.raises(ValueError):
            hsv_to_xyz(bad_hsv)

    def test_direct_hsl_hsv_preserves_hue(self) -> None:
        # Very light pastel that would suffer heavy hue quantization via 8-bit RGB
        hsv = hsl_to_hsv((213.45, 0.3, 0.96))
        assert hsv[0] == 213.45
        hsl_back = hsv_to_hsl(hsv)
        assert hsl_back[0] == 213.45
        # Achromatic edge cases
        assert hsl_to_hsv((180, 0.0, 0.5)) == (0.0, 0.0, 0.5)
        assert hsl_to_hsv((180, 1.0, 0.0)) == (0.0, 0.0, 0.0)
        assert hsv_to_hsl((180, 0.0, 1.0)) == (0.0, 0.0, 1.0)
        assert hsv_to_hsl((180, 1.0, 0.0)) == (0.0, 0.0, 0.0)

    def test_cmyk_conversions_and_validation(self) -> None:
        assert rgb_to_cmyk(0, 255, 255) == (1.0, 0.0, 0.0, 0.0)
        assert rgb_to_cmyk(0, 0, 0) == (0.0, 0.0, 0.0, 1.0)
        assert rgb_to_cmyk(255, 255, 255) == (0.0, 0.0, 0.0, 0.0)
        assert cmyk_to_rgb(0, 1, 1, 0) == (255, 0, 0)
        assert cmyk_to_rgb(0, 0, 0, 1) == (0, 0, 0)
        with pytest.raises(ValueError):
            cmyk_to_rgb(1.2, 0, 0, 0)
        with pytest.raises(ValueError):
            cmyk_to_xyz((0, -0.1, 0, 0))


class TestXyzAndLab:
    @pytest.mark.parametrize(
        "rgb",
        [
            (255, 0, 0),  # previously crashed with complex TypeError
            (0, 255, 0),  # previously crashed with complex TypeError
            (0, 0, 255),
            (0, 255, 255),  # previously drifted to (1, 255, 255)
            (255, 255, 0),
            (255, 0, 255),
            (0, 0, 0),
            (255, 255, 255),
            (5, 10, 15),  # exercises low-value sRGB linear segment (s <= 0.04045)
            (128, 64, 192),
        ],
    )
    def test_rgb_xyz_lab_exact_roundtrip(self, rgb: tuple[int, int, int]) -> None:
        xyz = rgb_to_xyz(*rgb)
        assert xyz_to_rgb(*xyz) == rgb

        lab = rgb_to_lab(*rgb)
        assert lab_to_rgb(*lab) == rgb

    def test_xyz_lab_grid_roundtrip(self) -> None:
        values = [0, 1, 5, 10, 11, 32, 64, 128, 192, 240, 255]
        for r in values:
            for g in (0, 10, 128, 255):
                for b in (0, 10, 128, 255):
                    assert xyz_to_rgb(*rgb_to_xyz(r, g, b)) == (r, g, b)
                    assert lab_to_rgb(*rgb_to_lab(r, g, b)) == (r, g, b)

    def test_d65_white_and_black_reference(self) -> None:
        wx, wy, wz = rgb_to_xyz(255, 255, 255)
        assert (wx, wy, wz) == pytest.approx((0.95047, 1.0, 1.08883), abs=1e-5)
        assert rgb_to_xyz(0, 0, 0) == (0.0, 0.0, 0.0)

        wl, wa, wb = rgb_to_lab(255, 255, 255)
        assert (wl, wa, wb) == pytest.approx((100.0, 0.0, 0.0), abs=1e-4)
        assert rgb_to_lab(0, 0, 0) == pytest.approx((0.0, 0.0, 0.0), abs=1e-6)

        assert lab_to_xyz((100.0, 0.0, 0.0)) == pytest.approx((0.95047, 1.0, 1.08883), abs=1e-5)
        assert xyz_to_lab((0.95047, 1.0, 1.08883)) == pytest.approx((100.0, 0.0, 0.0), abs=1e-5)

    def test_xyz_lab_validation(self) -> None:
        with pytest.raises(ValueError):
            rgb_to_xyz(-1, 0, 0)
        with pytest.raises(ValueError):
            xyz_to_rgb(-0.1, 0.0, 0.0)
        with pytest.raises(ValueError):
            lab_to_rgb(101.0, 0.0, 0.0)
        with pytest.raises(ValueError):
            lab_to_rgb(-1.0, 0.0, 0.0)

    def test_linear_rgb_roundtrip_all_256(self) -> None:
        for v in range(256):
            lin = rgb_to_linear((v, v, v))
            assert linear_to_rgb(lin) == (v, v, v)
        with pytest.raises(ValueError):
            linear_to_rgb((1.5, 0.0, 0.0))


class TestCrossSpaceMatrix:
    def test_all_cross_conversions_for_red(self) -> None:
        assert hsl_to_hex((0, 1, 0.5)) == "#FF0000"
        assert hsv_to_hex((0, 1, 1)) == "#FF0000"
        assert cmyk_to_hex((0, 1, 1, 0)) == "#FF0000"

        assert hex_to_hsl("#FF0000") == (0.0, 1.0, 0.5)
        assert hex_to_hsv("#FF0000") == (0.0, 1.0, 1.0)
        assert hex_to_cmyk("#FF0000") == (0.0, 1.0, 1.0, 0.0)
        assert hsl_to_cmyk((0, 1, 0.5)) == (0.0, 1.0, 1.0, 0.0)
        assert hsv_to_cmyk((0, 1, 1)) == (0.0, 1.0, 1.0, 0.0)
        assert cmyk_to_hsl((0, 1, 1, 0)) == (0.0, 1.0, 0.5)
        assert cmyk_to_hsv((0, 1, 1, 0)) == (0.0, 1.0, 1.0)

        xyz = hex_to_xyz("#FF0000")
        assert xyz_to_hex(xyz) == "#FF0000"
        assert xyz_to_hsl(xyz) == (0.0, 1.0, 0.5)
        assert xyz_to_hsv(xyz) == (0.0, 1.0, 1.0)
        assert xyz_to_cmyk(xyz) == (0.0, 1.0, 1.0, 0.0)
        assert hsl_to_xyz((0, 1, 0.5)) == pytest.approx(xyz)
        assert hsv_to_xyz((0, 1, 1)) == pytest.approx(xyz)
        assert cmyk_to_xyz((0, 1, 1, 0)) == pytest.approx(xyz)

        lab = hex_to_lab("#FF0000")
        assert lab_to_hex(lab) == "#FF0000"
        assert lab_to_hsl(lab) == (0.0, 1.0, 0.5)
        assert lab_to_hsv(lab) == (0.0, 1.0, 1.0)
        assert lab_to_cmyk(lab) == (0.0, 1.0, 1.0, 0.0)
        assert hsl_to_lab((0, 1, 0.5)) == pytest.approx(lab)
        assert hsv_to_lab((0, 1, 1)) == pytest.approx(lab)
        assert cmyk_to_lab((0, 1, 1, 0)) == pytest.approx(lab)


class TestBlendingAndAdjustments:
    def test_blend_colors_srgb_and_linear(self) -> None:
        assert blend_colors((255, 0, 0), (0, 0, 255), 0.5) == (128, 0, 128)
        assert blend_colors((255, 0, 0), (0, 0, 255), 0.0) == (255, 0, 0)
        assert blend_colors((255, 0, 0), (0, 0, 255), 1.0) == (0, 0, 255)

        # Linear blending is brighter than naive sRGB blending for complementary primaries
        lin_mix = blend_colors((255, 0, 0), (0, 255, 0), 0.5, linear=True)
        assert lin_mix == (188, 188, 0)

    def test_blend_self_identity_all_values(self) -> None:
        # Regression: int() truncation previously turned blend_colors((3,3,3),(3,3,3),0.3) -> (2,2,2)
        for v in range(256):
            for ratio in (0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0):
                assert blend_colors((v, v, v), (v, v, v), ratio) == (v, v, v)

    def test_blend_validation(self) -> None:
        with pytest.raises(ValueError):
            blend_colors((255, 0, 0), (0, 0, 255), 1.5)
        with pytest.raises(ValueError):
            blend_colors((255, 0, 0), (0, 0, 255), -0.1)
        with pytest.raises(ValueError):
            blend_colors((300, 0, 0), (0, 0, 255), 0.5)

    def test_invert_grayscale_and_hsl_adjustments(self) -> None:
        assert invert_color((255, 0, 128)) == (0, 255, 127)
        assert invert_color((0, 0, 0)) == (255, 255, 255)

        gray = to_grayscale((255, 0, 0))
        assert gray[0] == gray[1] == gray[2]
        assert to_grayscale((120, 120, 120)) == (120, 120, 120)

        lighter = adjust_lightness((255, 0, 0), 0.25)
        assert lighter == (255, 128, 128)
        assert adjust_lightness((255, 0, 0), 1.0) == (255, 255, 255)
        assert adjust_lightness((255, 0, 0), -1.0) == (0, 0, 0)

        desaturated = adjust_saturation((255, 0, 0), -1.0)
        assert desaturated == (128, 128, 128)
        with pytest.raises(ValueError):
            adjust_lightness((255, 0, 0), 1.5)
        with pytest.raises(ValueError):
            adjust_saturation((255, 0, 0), -1.5)

    def test_top_level_reexports(self) -> None:
        assert hued.rgb_to_hex(255, 0, 0) == "#FF0000"
        assert hued.hex_to_rgb("#F00") == (255, 0, 0)


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
