"""Comprehensive unit tests for hued.colors."""

from __future__ import annotations

import re

import pytest

from hued.colors import ColorManager

# All 148 standard W3C CSS Color Level 4 named colors.
CSS_NAMED_COLORS = [
    "aliceblue", "antiquewhite", "aqua", "aquamarine", "azure", "beige", "bisque",
    "black", "blanchedalmond", "blue", "blueviolet", "brown", "burlywood", "cadetblue",
    "chartreuse", "chocolate", "coral", "cornflowerblue", "cornsilk", "crimson", "cyan",
    "darkblue", "darkcyan", "darkgoldenrod", "darkgray", "darkgreen", "darkgrey",
    "darkkhaki", "darkmagenta", "darkolivegreen", "darkorange", "darkorchid", "darkred",
    "darksalmon", "darkseagreen", "darkslateblue", "darkslategray", "darkslategrey",
    "darkturquoise", "darkviolet", "deeppink", "deepskyblue", "dimgray", "dimgrey",
    "dodgerblue", "firebrick", "floralwhite", "forestgreen", "fuchsia", "gainsboro",
    "ghostwhite", "gold", "goldenrod", "gray", "green", "greenyellow", "grey",
    "honeydew", "hotpink", "indianred", "indigo", "ivory", "khaki", "lavender",
    "lavenderblush", "lawngreen", "lemonchiffon", "lightblue", "lightcoral", "lightcyan",
    "lightgoldenrodyellow", "lightgray", "lightgreen", "lightgrey", "lightpink",
    "lightsalmon", "lightseagreen", "lightskyblue", "lightslategray", "lightslategrey",
    "lightsteelblue", "lightyellow", "lime", "limegreen", "linen", "magenta", "maroon",
    "mediumaquamarine", "mediumblue", "mediumorchid", "mediumpurple", "mediumseagreen",
    "mediumslateblue", "mediumspringgreen", "mediumturquoise", "mediumvioletred",
    "midnightblue", "mintcream", "mistyrose", "moccasin", "navajowhite", "navy",
    "oldlace", "olive", "olivedrab", "orange", "orangered", "orchid", "palegoldenrod",
    "palegreen", "paleturquoise", "palevioletred", "papayawhip", "peachpuff", "peru",
    "pink", "plum", "powderblue", "purple", "rebeccapurple", "red", "rosybrown",
    "royalblue", "saddlebrown", "salmon", "sandybrown", "seagreen", "seashell", "sienna",
    "silver", "skyblue", "slateblue", "slategray", "slategrey", "snow", "springgreen",
    "steelblue", "tan", "teal", "thistle", "tomato", "turquoise", "violet", "wheat",
    "white", "whitesmoke", "yellow", "yellowgreen",
]


class TestCatalogIntegrity:
    def test_all_entries_clean_unique_and_uppercase(self) -> None:
        cm = ColorManager()
        assert len(cm.color_list) >= 1300

        seen_names: set[str] = set()
        hex_pattern = re.compile(r"^#[0-9A-F]{6}$")

        for entry in cm.color_list:
            name = entry["name"]
            hx = entry["hex"]
            assert name == name.strip() and len(name) > 0
            assert "[" not in name and "]" not in name
            assert "citation" not in name.lower()
            assert "vomit" not in name.lower()
            assert hex_pattern.match(hx), f"Non-canonical hex {hx!r} for {name!r}"

            lower = name.lower()
            assert lower not in seen_names, f"Duplicate color name: {name!r}"
            seen_names.add(lower)

    def test_all_148_css_named_colors_resolve(self) -> None:
        cm = ColorManager()
        missing = [name for name in CSS_NAMED_COLORS if cm.get_color_by_name(name) is None]
        assert missing == []


class TestColorManagerMethods:
    def test_hex_rgb_helpers(self) -> None:
        cm = ColorManager()
        assert cm.hex_to_rgb("#FF5733") == (255, 87, 51)
        assert cm.hex_to_rgb("#F0A") == (255, 0, 170)
        assert cm.rgb_to_hex(0, 128, 0) == "#008000"

    def test_get_color_by_name_and_casing_preservation(self) -> None:
        cm = ColorManager()
        assert cm.get_color_by_name("Blue") == {
            "Name": "Blue",
            "Hex": "#0000FF",
            "RGB": (0, 0, 255),
        }
        assert cm.get_color_by_name("  green  ") == {
            "Name": "Green",
            "Hex": "#008000",
            "RGB": (0, 128, 0),
        }
        # Regression: .title() previously corrupted acronyms and apostrophes
        raf = cm.get_color_by_name("air force blue (raf)")
        assert raf is not None and raf["Name"] == "Air Force blue (RAF)"
        bdazzled = cm.get_color_by_name("b'dazzled blue")
        assert bdazzled is not None and bdazzled["Name"] == "B'dazzled blue"
        # Cleaned citation artifacts
        assert cm.get_color_by_name("Cinnamon") == {
            "Name": "Cinnamon",
            "Hex": "#D2691E",
            "RGB": (210, 105, 30),
        }
        assert cm.get_color_by_name("nonexistent color xyz") is None
        assert cm.get_color_by_name("   ") is None

    def test_closest_color_name_modes(self) -> None:
        cm = ColorManager()
        assert cm.closest_color_name("#FF0000") == "Red"
        assert cm.closest_color_name("#F00") == "Red"
        assert cm.closest_color_name("#FF0000", space="lab") == "Red"
        assert cm.closest_color_name("#FF0000", space="cie2000") == "Red"

        # Slightly perturbed color resolves consistently in all spaces
        assert isinstance(cm.closest_color_name("#FE0502", space="rgb"), str)
        assert isinstance(cm.closest_color_name("#FE0502", space="lab"), str)
        assert isinstance(cm.closest_color_name("#FE0502", space="cie2000"), str)

        with pytest.raises(ValueError):
            cm.closest_color_name("#FF0000", space="unknown")

    def test_get_color_by_hex_search_and_random(self) -> None:
        cm = ColorManager()
        assert cm.get_color_by_hex("#ff0000") == {
            "Name": "Red",
            "Hex": "#FF0000",
            "RGB": (255, 0, 0),
        }
        assert cm.get_color_by_hex("#123456") is None

        matches = cm.search_colors("cerulean")
        assert len(matches) >= 5
        assert all("cerulean" in m["Name"].lower() for m in matches)
        assert cm.search_colors("") == []

        rand = cm.get_random_color()
        assert set(rand.keys()) == {"Name", "Hex", "RGB"}

    def test_add_remove_and_instance_isolation(self) -> None:
        cm1 = ColorManager()
        cm2 = ColorManager()

        added = cm1.add_color("Infinitode Violet", "#5d17eb")
        assert added == {
            "Name": "Infinitode Violet",
            "Hex": "#5D17EB",
            "RGB": (93, 23, 235),
        }
        assert cm1.get_color_by_name("infinitode violet") == added
        assert cm2.get_color_by_name("infinitode violet") is None

        # Updating an existing custom color overwrites in place
        updated = cm1.add_color("infinitode violet", "#6020F0")
        assert updated["Hex"] == "#6020F0"

        assert cm1.remove_color("INFINITODE VIOLET") is True
        assert cm1.remove_color("INFINITODE VIOLET") is False
        assert cm1.get_color_by_name("infinitode violet") is None

        with pytest.raises(ValueError):
            cm1.add_color("   ", "#FFFFFF")


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
