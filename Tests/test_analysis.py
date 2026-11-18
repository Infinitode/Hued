"""Comprehensive unit tests for hued.analysis."""

from __future__ import annotations

import pytest

from hued.analysis import (
    _ciede2000,
    brightness,
    check_color_quality,
    check_wcag_contrast,
    color_contrast,
    delta_e,
    get_luminance,
    get_temperature,
    get_text_color_from_background,
    get_vibrancy,
    is_muted,
    is_neutral,
    is_pastel,
    is_vibrant,
    rgb_to_linear,
    simulate_color_blindness,
)


class TestColorProperties:
    @pytest.mark.parametrize(
        ("rgb", "expected"),
        [
            ((255, 0, 0), "Warm"),
            ((255, 165, 0), "Warm"),
            ((255, 255, 0), "Warm"),  # regression: yellow was previously "Neutral"
            ((255, 0, 64), "Warm"),
            ((0, 0, 255), "Cool"),
            ((0, 255, 255), "Cool"),  # regression: cyan was previously "Neutral"
            ((0, 128, 128), "Cool"),  # regression: teal was previously "Neutral"
            ((0, 180, 120), "Cool"),
            ((128, 128, 128), "Neutral"),
            ((0, 0, 0), "Neutral"),
            ((255, 255, 255), "Neutral"),
            ((130, 128, 128), "Neutral"),  # regression: near-gray was previously "Warm"
            ((0, 255, 0), "Neutral"),
            ((255, 0, 255), "Neutral"),
        ],
    )
    def test_get_temperature(self, rgb: tuple[int, int, int], expected: str) -> None:
        assert get_temperature(rgb) == expected

    def test_is_neutral(self) -> None:
        assert is_neutral((128, 128, 128)) is True
        assert is_neutral((140, 125, 130)) is True
        assert is_neutral((255, 0, 0)) is False
        assert is_neutral((140, 125, 130), tolerance=10) is False
        with pytest.raises(ValueError):
            is_neutral((128, 128, 128), tolerance=-1)

    def test_brightness(self) -> None:
        assert brightness((255, 255, 255)) == pytest.approx(1.0)
        assert brightness((0, 0, 0)) == 0.0
        assert brightness((255, 0, 0)) == pytest.approx(0.299)
        assert brightness((0, 255, 0)) == pytest.approx(0.587)
        assert brightness((0, 0, 255)) == pytest.approx(0.114)

    def test_is_pastel(self) -> None:
        assert is_pastel((255, 200, 200)) is True
        assert is_pastel((174, 198, 207)) is True  # pastel blue
        assert is_pastel((119, 221, 119)) is True  # pastel green (channel <= 127)
        assert is_pastel((230, 230, 250)) is True  # lavender
        assert is_pastel((253, 253, 150)) is True  # pastel yellow
        # Non-pastels (including regressions for white and light gray)
        assert is_pastel((255, 255, 255)) is False
        assert is_pastel((220, 220, 220)) is False
        assert is_pastel((255, 0, 0)) is False
        assert is_pastel((0, 255, 255)) is False
        assert is_pastel((50, 50, 50)) is False

    def test_is_muted(self) -> None:
        assert is_muted((100, 100, 100)) is True
        assert is_muted((112, 128, 144)) is True  # slate gray
        assert is_muted((143, 151, 121)) is True  # sage green
        assert is_muted((180, 130, 140)) is True  # dusty rose
        # Non-muted
        assert is_muted((0, 0, 0)) is False
        assert is_muted((255, 255, 255)) is False
        assert is_muted((255, 200, 200)) is False  # pastel
        assert is_muted((255, 0, 0)) is False

    def test_is_vibrant_and_get_vibrancy(self) -> None:
        assert is_vibrant((0, 255, 0)) is True
        assert is_vibrant((255, 80, 0)) is True
        assert is_vibrant((128, 128, 128)) is False
        assert is_vibrant((80, 0, 0)) is False

        assert get_vibrancy((0, 0, 0)) == 0.0
        assert get_vibrancy((255, 255, 255)) == 0.0
        assert get_vibrancy((255, 0, 0)) == 1.0


class TestLuminanceAndWcag:
    def test_rgb_to_linear_wcag_spec(self) -> None:
        # Low-value linear branch s <= 0.04045 (c = 10 -> s = 10/255 = 0.039215686)
        low = rgb_to_linear((10, 0, 255))
        assert low[0] == pytest.approx((10.0 / 255.0) / 12.92, rel=1e-12)
        assert low[1] == 0.0
        assert low[2] == 1.0

        # Gamma branch s > 0.04045 (c = 128)
        mid = rgb_to_linear((128, 128, 128))
        expected_mid = ((128.0 / 255.0 + 0.055) / 1.055) ** 2.4
        assert mid == pytest.approx([expected_mid, expected_mid, expected_mid], rel=1e-12)

    def test_luminance_and_contrast_wcag(self) -> None:
        assert get_luminance((0, 0, 0)) == 0.0
        assert get_luminance((255, 255, 255)) == pytest.approx(1.0)
        assert get_luminance((255, 0, 0)) == pytest.approx(0.2126)
        assert get_luminance((0, 255, 0)) == pytest.approx(0.7152)
        assert get_luminance((0, 0, 255)) == pytest.approx(0.0722)

        assert color_contrast((0, 0, 0), (255, 255, 255)) == pytest.approx(21.0)
        assert color_contrast((255, 255, 255), (0, 0, 0)) == pytest.approx(21.0)
        assert color_contrast((100, 150, 200), (100, 150, 200)) == pytest.approx(1.0)
        # WCAG 2.1 exact contrast between pure green and mid-gray (#808080)
        assert color_contrast((0, 255, 0), (128, 128, 128)) == pytest.approx(2.8782, rel=1e-3)

    def test_check_wcag_contrast(self) -> None:
        high = check_wcag_contrast((0, 0, 0), (255, 255, 255))
        assert high == {
            "contrast_ratio": 21.0,
            "aa_normal": True,
            "aa_large": True,
            "aaa_normal": True,
            "aaa_large": True,
            "ui_components": True,
        }
        low = check_wcag_contrast((200, 200, 200), (255, 255, 255))
        assert low["aa_normal"] is False
        assert low["aa_large"] is False
        assert low["ui_components"] is False

    @pytest.mark.parametrize(
        ("bg", "expected"),
        [
            ((0, 0, 0), "light"),  # regression: previously returned "dark"
            ((30, 30, 30), "light"),  # regression: previously returned "dark"
            ((0, 0, 255), "light"),
            ((80, 20, 120), "light"),
            ((255, 255, 255), "dark"),
            ((255, 255, 0), "dark"),  # regression: previously returned "light"
            ((0, 255, 255), "dark"),  # regression: previously returned "light"
            ((0, 255, 0), "dark"),  # regression: previously returned "light"
            ((180, 180, 180), "dark"),  # regression: previously returned "light"
        ],
    )
    def test_get_text_color_from_background(self, bg: tuple[int, int, int], expected: str) -> None:
        assert get_text_color_from_background(bg) == expected

    def test_text_color_always_maximizes_wcag_contrast(self) -> None:
        steps = [0, 32, 64, 96, 128, 160, 192, 224, 255]
        for r in steps:
            for g in (0, 85, 170, 255):
                for b in (0, 85, 170, 255):
                    choice = get_text_color_from_background((r, g, b))
                    chosen_rgb = (255, 255, 255) if choice == "light" else (0, 0, 0)
                    other_rgb = (0, 0, 0) if choice == "light" else (255, 255, 255)
                    assert color_contrast((r, g, b), chosen_rgb) >= color_contrast(
                        (r, g, b), other_rgb
                    )

    def test_check_color_quality(self) -> None:
        navy = check_color_quality((0, 0, 128))
        assert navy["is_good_quality"] is True
        assert navy["best_background"] == "white"
        assert navy["passes_aaa_on_white"] is True

        # Mid-gray lacks 7:1 contrast against both black (5.32) and white (3.95)
        mid_gray = check_color_quality((128, 128, 128))
        assert mid_gray["is_good_quality"] is False
        assert mid_gray["passes_aa_on_black"] is True
        assert mid_gray["passes_aa_on_white"] is False

        # Against a specific background, defaults to WCAG AA (4.5:1)
        on_white = check_color_quality((180, 180, 180), background=(255, 255, 255))
        assert on_white["is_good_quality"] is False
        assert on_white["contrast_with_background"] < 4.5

        on_black = check_color_quality((180, 180, 180), background=(0, 0, 0))
        assert on_black["is_good_quality"] is True
        assert on_black["contrast_with_background"] >= 4.5

        with pytest.raises(ValueError):
            check_color_quality((0, 0, 0), min_contrast=0.5)


class TestColorBlindnessAndDeltaE:
    @pytest.mark.parametrize(
        "mode", ["protanopia", "deuteranopia", "tritanopia", "achromatopsia"]
    )
    def test_neutral_grays_are_invariant(self, mode: str) -> None:
        for v in (0, 1, 10, 29, 64, 128, 200, 255):
            for intensity in (0.0, 0.3, 0.5, 1.0):
                assert simulate_color_blindness((v, v, v), mode, intensity) == (v, v, v)

    def test_color_blindness_behavior_and_validation(self) -> None:
        sample = (220, 50, 80)
        assert simulate_color_blindness(sample, "PROTANOPIA", 0.0) == sample

        achro = simulate_color_blindness(sample, "achromatopsia", 1.0)
        assert achro[0] == achro[1] == achro[2]

        with pytest.raises(ValueError):
            simulate_color_blindness(sample, "unknown")
        with pytest.raises(ValueError):
            simulate_color_blindness(sample, "protanopia", 1.5)
        with pytest.raises(TypeError):
            simulate_color_blindness(sample, "protanopia", True)  # type: ignore[arg-type]

    @pytest.mark.parametrize(
        ("lab1", "lab2", "expected"),
        [
            # Official Sharma, Wu & Dalal (2005) CIEDE2000 reference test vectors
            ((50.0000, 2.6772, -79.7751), (50.0000, 0.0000, -82.7485), 2.0425),
            ((50.0000, 3.1571, -77.2803), (50.0000, 0.0000, -82.7485), 2.8615),
            ((50.0000, -1.3802, -84.2814), (50.0000, 0.0000, -82.7485), 1.0000),
            ((50.0000, 0.0000, 0.0000), (50.0000, -1.0000, 2.0000), 2.3669),
            ((50.0000, 2.5000, 0.0000), (73.0000, 25.0000, -18.0000), 27.1492),
            ((60.2574, -34.0099, 36.2677), (60.4626, -34.1751, 39.4387), 1.2644),
            ((2.0776, 0.0795, -1.1350), (0.9033, -0.0636, -0.5514), 0.9082),
        ],
    )
    def test_ciede2000_sharma_reference_vectors(
        self,
        lab1: tuple[float, float, float],
        lab2: tuple[float, float, float],
        expected: float,
    ) -> None:
        assert _ciede2000(lab1, lab2) == pytest.approx(expected, abs=1e-4)

    def test_delta_e_public_api(self) -> None:
        assert delta_e((120, 80, 200), (120, 80, 200)) == 0.0
        assert delta_e((120, 80, 200), (120, 80, 200), method="cie76") == 0.0
        # Symmetry
        d1 = delta_e((255, 0, 0), (0, 128, 255))
        d2 = delta_e((0, 128, 255), (255, 0, 0))
        assert d1 == pytest.approx(d2)
        # Subtle difference << opposite colors
        assert delta_e((100, 100, 100), (102, 100, 100)) < 2.0
        assert delta_e((0, 0, 0), (255, 255, 255)) == pytest.approx(100.0, abs=0.1)
        assert delta_e((0, 0, 0), (255, 255, 255), method="cie76") == pytest.approx(100.0, abs=1e-3)

        with pytest.raises(ValueError):
            delta_e((0, 0, 0), (255, 255, 255), method="invalid")


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
